import requests
from extruct import extract
from w3lib.html import get_base_url

def detect_structured_data(url):
    r = requests.get(url)
    base = get_base_url(r.text, r.url)
    # estrai tutti i formati strutturati supportati
    metadata = extract(r.text, base_url=base, syntaxes=['json-ld','microdata','opengraph','rdfa'])
    # controlla quali tipi sono presenti
    formats = {fmt: bool(metadata.get(fmt)) for fmt in ['json-ld','microdata','opengraph','rdfa']} 
    return formats

if __name__ == "__main__":
    url = input("Inserisci l'URL: ")
    result = detect_structured_data(url)
    print("\nFormati strutturati rilevati:")
    for fmt, found in result.items():
        print(f"• {fmt}: {'✅ presente' if found else '❌ assente'}")
