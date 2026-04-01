from sys import argv
from getrails import search
from urllib.parse import urlparse

def url_to_dork(url):
    parsed = urlparse(url)
    host = parsed.netloc or parsed.path
    return f"site:{host}"

results = search(url_to_dork(argv[1]))
if not results:
    print(f"[WARN] Nenhuma URL encontrada para {argv[1]}", flush=True)
else:
    print("\n".join(results))
