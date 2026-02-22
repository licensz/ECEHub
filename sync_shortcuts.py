import json
import requests
import sys

# Verifizierte, aktuelle Quellen (Stand 2025)
SOURCES = [
    "https://raw.githubusercontent.com",
    "https://raw.githubusercontent.com"
]

def transform():
    raw_data = None
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    for url in SOURCES:
        try:
            print(f"Versuche Quelle: {url}")
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200 and "application/json" in response.headers.get("Content-Type", ""):
                raw_data = response.json()
                print("Quelle erfolgreich geladen!")
                break
        except Exception as e:
            print(f"Fehler bei {url}: {e}")

    if not raw_data:
        print("KRITISCH: Keine valide JSON-Quelle gefunden.")
        sys.exit(1)

    transformed = []
    
    # Rekursiver Parser für verschachtelte Strukturen
    def parse_data(obj, cat="Allgemein"):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, str) and "prefs:" in value:
                    transformed.append({
                        "name": key,
                        "category": cat,
                        "iconName": "gearshape.fill",
                        "description": f"iOS Einstellungen für {key}",
                        "urlScheme": value.replace("prefs:", "App-prefs:"),
                        "keywords": [key.lower(), cat.lower()]
                    })
                else:
                    parse_data(value, key)
        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, dict):
                    name = item.get('title') or item.get('name') or "Unbekannt"
                    url = item.get('url') or ""
                    if "prefs:" in url:
                        transformed.append({
                            "name": name,
                            "category": cat,
                            "iconName": "gearshape.fill",
                            "description": f"Direktzugriff auf {name}",
                            "urlScheme": url.replace("prefs:", "App-prefs:"),
                            "keywords": [name.lower()]
                        })

    parse_data(raw_data)

    if transformed:
        with open('ecehub_master.json', 'w', encoding='utf-8') as f:
            json.dump(transformed, f, indent=2, ensure_ascii=False)
        print(f"ERFOLG: {len(transformed)} Shortcuts in ecehub_master.json gespeichert.")
    else:
        sys.exit("Keine passenden URLs in der Quelle gefunden.")

if __name__ == "__main__":
    transform()
