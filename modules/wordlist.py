"""
modules/wordlist.py — D4N155 Improved
Geração de wordlist a partir de texto bruto ou palavras coletadas pelo scraper.

Melhorias implementadas:
  - collections.Counter (implementado em C) no lugar de dict manual
  - Processamento em streaming linha-a-linha (sem carregar tudo na RAM)
  - Deduplicação antecipada com set() antes de qualquer ordenação
  - Pipeline funcional: texto → tokens → filtro → rank → mutações (GoMutation)
  - Suporte a --based (arquivo de texto estático) com fix do bug issue #17
  - Normalização unicode para lidar com acentos corretamente
"""

import os
import re
import subprocess
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Iterator, Optional

# ──────────────────────────────────────────────
# Configurações
# ──────────────────────────────────────────────
MIN_WORD_LEN = 3
MAX_WORD_LEN = 32
TOP_N_WORDS = 5000          # palavras mais frequentes a manter
GOMUTATION_BIN = Path(__file__).parent / "GoMutation"


# ──────────────────────────────────────────────
# Normalização de texto
# ──────────────────────────────────────────────
def normalize(text: str) -> str:
    """
    Remove acentos, converte para lowercase.
    unicodedata.normalize garante compatibilidade com Python 3.10+.
    """
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).lower()


def tokenize(text: str) -> Iterator[str]:
    """
    Gerador: divide texto em tokens válidos sem criar lista intermediária.
    Filtra por tamanho mínimo e máximo. Deduplicação ocorre no Counter.
    """
    for word in re.split(r"[\s\W]+", text):
        word = normalize(word)
        if MIN_WORD_LEN <= len(word) <= MAX_WORD_LEN and word.isalnum():
            yield word


# ──────────────────────────────────────────────
# Streaming de arquivo (fix bug issue #17)
# ──────────────────────────────────────────────
def stream_file(path: str) -> Iterator[str]:
    """
    Lê arquivo linha-a-linha (streaming) sem carregar tudo na memória.
    Corrige o bug #17: textos estáticos no modo interativo não eram salvos
    porque o arquivo era lido de uma vez e falhava silenciosamente em
    arquivos grandes ou com encoding inesperado.
    """
    filepath = Path(path)
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with filepath.open("r", encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            yield line


# ──────────────────────────────────────────────
# Construção do Counter a partir de fonte
# ──────────────────────────────────────────────
def build_counter_from_words(words: list) -> Counter:
    """Constrói Counter a partir de lista já tokenizada (vinda do scraper)."""
    return Counter(words)


def build_counter_from_text(text: str) -> Counter:
    """Constrói Counter a partir de texto bruto. Usa gerador (sem lista intermediária)."""
    return Counter(tokenize(text))


def build_counter_from_file(path: str) -> Counter:
    """
    Constrói Counter via streaming de arquivo.
    Nunca carrega o arquivo inteiro na memória.
    """
    counter: Counter = Counter()
    for line in stream_file(path):
        counter.update(tokenize(line))
    return counter


# ──────────────────────────────────────────────
# Filtragem e ranking
# ──────────────────────────────────────────────
def top_words(counter: Counter, n: int = TOP_N_WORDS) -> list:
    """
    Retorna as N palavras mais frequentes como lista ordenada.
    Counter.most_common() é O(n log n) em C — muito mais rápido que sort() puro.
    """
    return [word for word, _ in counter.most_common(n)]


# ──────────────────────────────────────────────
# Integração com GoMutation (mantido intacto)
# ──────────────────────────────────────────────
def apply_gomutation(words: list) -> list:
    """
    Passa a wordlist pelo binário GoMutation para geração de variações.
    GoMutation é preservado conforme solicitado — sem alterações.
    Melhoria: usa subprocess com stdin pipe em vez de arquivo temporário,
    reduzindo I/O de disco.
    """
    if not GOMUTATION_BIN.exists():
        print(
            f"[WARN] GoMutation binary not found at {GOMUTATION_BIN}. "
            "Skipping mutation step. Run 'go build' first.",
            file=sys.stderr,
        )
        return words

    input_data = "\n".join(words).encode("utf-8")

    try:
        result = subprocess.run(
            [str(GOMUTATION_BIN)],
            input=input_data,
            capture_output=True,
            timeout=120,
        )
        if result.returncode == 0:
            mutated = result.stdout.decode("utf-8", errors="ignore").splitlines()
            # Deduplicação pós-mutação com set, mantendo a ordem via dict trick
            seen: dict = {}
            for w in words + mutated:
                seen[w] = None
            return list(seen.keys())
        else:
            print(
                f"[WARN] GoMutation exited with code {result.returncode}",
                file=sys.stderr,
            )
            return words
    except subprocess.TimeoutExpired:
        print("[WARN] GoMutation timed out. Returning unmodified wordlist.", file=sys.stderr)
        return words
    except Exception as exc:
        print(f"[WARN] GoMutation error: {exc}", file=sys.stderr)
        return words


# ──────────────────────────────────────────────
# Saída para arquivo (fix bug #17: salva corretamente)
# ──────────────────────────────────────────────
def save_wordlist(words: list, output_path: str) -> None:
    """
    Salva a wordlist no arquivo de saída.
    Fix bug #17: garante flush e close explícitos para evitar perda de dados
    no modo interativo que encerrava sem dar tempo ao buffer de descarregar.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as fh:
        for word in words:
            fh.write(word + "\n")
        fh.flush()
        os.fsync(fh.fileno())   # garante escrita mesmo em interrupção

    print(f"[OK] Wordlist saved: {output_path} ({len(words)} words)")


# ──────────────────────────────────────────────
# Função principal de geração
# ──────────────────────────────────────────────
def generate(
    words: Optional[list] = None,
    text: Optional[str] = None,
    based_file: Optional[str] = None,
    output: Optional[str] = None,
    top_n: int = TOP_N_WORDS,
    mutate: bool = True,
) -> list:
    """
    Pipeline completo de geração de wordlist.

    Fontes aceitas (podem ser combinadas):
      - words:      lista já tokenizada (vinda do scraper assíncrono)
      - text:       texto bruto em memória
      - based_file: caminho para arquivo de texto (--based)

    Retorna lista final de palavras.
    """
    counter: Counter = Counter()

    if words:
        counter.update(build_counter_from_words(words))

    if text:
        counter.update(build_counter_from_text(text))

    if based_file:
        counter.update(build_counter_from_file(based_file))

    if not counter:
        print("[WARN] No input provided to wordlist generator.", file=sys.stderr)
        return []

    ranked = top_words(counter, n=top_n)

    if mutate:
        ranked = apply_gomutation(ranked)

    if output:
        save_wordlist(ranked, output)

    return ranked


# ──────────────────────────────────────────────
# CLI de teste rápido
# ──────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 wordlist.py <text_file> [output_file]")
        sys.exit(1)

    based = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    result = generate(based_file=based, output=out, mutate=False)
    if not out:
        print("\n".join(result))
