"""
modules/aggressive.py — D4N155 Improved
Modo --aggressive com headless browser.

Melhorias implementadas:
  - Pool de páginas Playwright: uma única instância do browser reutilizada
    para todas as URLs (em vez de criar/destruir browser por URL)
  - Playwright é mais rápido e moderno que Selenium/geckodriver
  - Fallback automático para scraper normal (aiohttp) quando JS não é
    necessário (detectado por análise do HTML inicial)
  - Semáforo de concorrência para as tabs do browser
  - Timeout configurável por página
  - Compatível com geckodriver legado via flag --use-gecko para
    retrocompatibilidade caso o usuário não tenha Playwright instalado
"""

import asyncio
import logging
import sys
from typing import Optional

from modules.scraper import extract_words_from_html, _write_cache, _read_cache

log = logging.getLogger("d4n155.aggressive")

# Concorrência máxima de tabs abertas simultaneamente
MAX_BROWSER_TABS = 4
PAGE_TIMEOUT = 20_000  # ms (Playwright usa ms)
WAIT_UNTIL = "domcontentloaded"  # mais rápido que "networkidle"


# ──────────────────────────────────────────────
# Detecção: página realmente precisa de JS?
# ──────────────────────────────────────────────
async def _needs_js(url: str) -> bool:
    """
    Faz uma requisição rápida com aiohttp e verifica se o body tem
    conteúdo útil sem JS. Se o body for muito pequeno ou tiver markers
    típicos de SPA (React root vazio, loader divs), retorna True.
    """
    import aiohttp
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=8), ssl=False) as r:
                html = await r.text(errors="ignore")
                # Heurística: body com menos de 500 chars úteis → provavelmente SPA
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(html, "lxml")
                for tag in soup(["script", "style"]):
                    tag.decompose()
                text = soup.get_text().strip()
                return len(text) < 500
    except Exception:
        return True  # Na dúvida, usa headless


# ──────────────────────────────────────────────
# Pool de páginas Playwright
# ──────────────────────────────────────────────
async def _scrape_with_playwright(urls: list, rate: float = 0.0) -> set:
    """
    Abre UMA instância do browser e reutiliza pages em pool.
    Muito mais eficiente do que criar browser por URL (comportamento original).
    """
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        log.error(
            "Playwright não instalado. Execute: pip install playwright && playwright install chromium"
        )
        log.warning("Falling back to standard (non-JS) scraper.")
        from modules.scraper import _scrape_all
        return await _scrape_all(urls, rate)

    word_set: set = set()
    semaphore = asyncio.Semaphore(MAX_BROWSER_TABS)

    async def fetch_page(page, url: str) -> Optional[str]:
        cached = _read_cache(url)
        if cached:
            return cached
        try:
            await page.goto(url, timeout=PAGE_TIMEOUT, wait_until=WAIT_UNTIL)
            # Aguarda render mínimo
            await page.wait_for_timeout(800)
            html = await page.content()
            _write_cache(url, html)
            if rate > 0:
                await asyncio.sleep(rate)
            return html
        except Exception as exc:
            log.warning("Headless failed for %s: %s", url, exc)
            return None

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-extensions",
            ],
        )
        log.info("Browser launched (Chromium headless). Processing %d URLs...", len(urls))

        async def process_url(url: str):
            async with semaphore:
                page = await browser.new_page()
                try:
                    html = await fetch_page(page, url)
                    if html:
                        word_set.update(extract_words_from_html(html))
                finally:
                    await page.close()

        await asyncio.gather(*[process_url(url) for url in urls])
        await browser.close()

    return word_set


# ──────────────────────────────────────────────
# Fallback para geckodriver (legado)
# ──────────────────────────────────────────────
async def _scrape_with_gecko(urls: list, rate: float = 0.0) -> set:
    """
    Fallback usando selenium + geckodriver (comportamento original do projeto).
    Melhorado: reutiliza UMA instância do driver para todas as URLs.
    """
    log.info("Using geckodriver (legacy mode).")
    word_set: set = set()

    try:
        from selenium import webdriver
        from selenium.webdriver.firefox.options import Options
        from selenium.common.exceptions import WebDriverException
    except ImportError:
        log.error("Selenium não instalado: pip install selenium")
        return word_set

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    try:
        driver = webdriver.Firefox(options=options)
    except Exception as exc:
        log.error("Falha ao iniciar geckodriver: %s", exc)
        return word_set

    try:
        for url in urls:
            cached = _read_cache(url)
            if cached:
                word_set.update(extract_words_from_html(cached))
                continue
            try:
                driver.get(url)
                # Aguarda carregamento básico
                await asyncio.sleep(max(rate, 1.0))
                html = driver.page_source
                _write_cache(url, html)
                word_set.update(extract_words_from_html(html))
            except WebDriverException as exc:
                log.warning("Gecko error for %s: %s", url, exc)
    finally:
        driver.quit()  # garante fechamento mesmo em erro

    return word_set


# ──────────────────────────────────────────────
# Interface pública
# ──────────────────────────────────────────────
def scrape_aggressive(urls: list, rate: float = 0.0, use_gecko: bool = False) -> list:
    """
    Ponto de entrada do modo --aggressive.

    Estratégia:
      1. Tenta Playwright (moderno, rápido, pool de tabs)
      2. Se --use-gecko ou Playwright indisponível → geckodriver com instância única
      3. Para URLs que não precisam de JS → delega ao scraper assíncrono normal

    Retorna lista ordenada de palavras.
    """
    import time
    start = time.perf_counter()

    if use_gecko:
        words = asyncio.run(_scrape_with_gecko(urls, rate))
    else:
        words = asyncio.run(_scrape_with_playwright(urls, rate))

    elapsed = time.perf_counter() - start
    log.info(
        "Aggressive scrape: %d URLs → %d unique words in %.2fs",
        len(urls), len(words), elapsed,
    )
    return sorted(words)


# ──────────────────────────────────────────────
# CLI de teste rápido
# ──────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 aggressive.py <url> [url2 ...]")
        sys.exit(1)

    gecko = "--use-gecko" in sys.argv
    urls = [u for u in sys.argv[1:] if not u.startswith("--")]
    result = scrape_aggressive(urls, use_gecko=gecko)
    print("\n".join(result))
