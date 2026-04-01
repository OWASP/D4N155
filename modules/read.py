"""
modules/read.py — D4N155
Extração de texto de uma URL para alimentar o blob.txt.
Modo 0 (static):     requests + BeautifulSoup/lxml
Modo 1 (aggressive): Playwright (substitui Selenium/geckodriver)
"""
import re
import sys
from bs4 import BeautifulSoup

PAGE_LOAD_TIMEOUT = 30_000  # ms (Playwright usa milissegundos)
STATIC_TIMEOUT    = 15      # segundos (requests)

# ── Normaliza e valida URL ─────────────────────────────────────────
def _normalize(url: str) -> str:
    url = url.strip()
    # Remove apenas barras duplas sem schema
    url = re.sub(r'^//', '', url)
    if not url:
        raise ValueError("Empty URL after normalization")
    # Injeta http:// APENAS se não tiver schema nenhum
    if not re.match(r'^https?://', url):
        url = 'http://' + url
    return url

def _is_valid_url(url: str) -> bool:
    try:
        # Remove schema para verificar se sobrou host
        host = re.sub(r'^https?://', '', _normalize(url)).split('/')[0]
        return len(host) > 0
    except ValueError:
        return False

# ── Extração de texto visível ──────────────────────────────────────
def _extract_text(html: str) -> str:
    try:
        soup = BeautifulSoup(html, 'lxml')
    except Exception:
        soup = BeautifulSoup(html, 'html.parser')
    for tag in soup(['script', 'style', 'noscript', 'head',
                     'nav', 'footer', 'aside']):
        tag.decompose()
    return soup.get_text(separator=' ', strip=True)

# ── Modo estático (requests) ───────────────────────────────────────
def static_read(url: str) -> str:
    import requests
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/120.0 Safari/537.36'
        )
    }
    try:
        resp = requests.get(url, headers=headers, timeout=STATIC_TIMEOUT, verify=False)
        resp.raise_for_status()
        return _extract_text(resp.text)
    except Exception as e:
        print(f'[WARN] static_read failed for {url}: {e}', file=sys.stderr)
        return ''

# ── Modo agressivo (Playwright) ────────────────────────────────────
def aggressive_read(url: str) -> str:
    import asyncio

    async def _fetch():
        try:
            from playwright.async_api import async_playwright
        except ImportError:
            print('[WARN] Playwright não instalado, usando static_read', file=sys.stderr)
            return static_read(url)

        async with async_playwright() as pw:
            browser = await pw.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"],
            )
            page = await browser.new_page()
            try:
                await page.goto(url, timeout=PAGE_LOAD_TIMEOUT, wait_until="domcontentloaded")
                await page.wait_for_timeout(800)
                html = await page.content()
                return _extract_text(html)
            except Exception as e:
                print(f'[WARN] Playwright timeout/error for {url}: {e} — trying partial content', file=sys.stderr)
                try:
                    html = await page.content()
                    return _extract_text(html)
                except Exception:
                    return static_read(url)
            finally:
                await page.close()
                await browser.close()

    try:
        return asyncio.run(_fetch())
    except Exception as e:
        print(f'[WARN] aggressive_read failed for {url}: {e}', file=sys.stderr)
        return static_read(url)

# ── Entry point ────────────────────────────────────────────────────
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: read.py <url> <0|1>', file=sys.stderr)
        sys.exit(1)

    raw  = sys.argv[1]
    mode = sys.argv[2]

    if not _is_valid_url(raw):
        print(f'[WARN] Skipping invalid URL: {raw!r}', file=sys.stderr)
        sys.exit(0)

    url  = _normalize(raw)
    text = aggressive_read(url) if mode == '1' else static_read(url)
    print(text)
