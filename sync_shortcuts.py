import json
import requests
import sys

# Wir nutzen stabile URLs und einen "User-Agent", um Blockaden zu umgehen
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)"}
SOURCES = [
    "https://raw.githubusercontent.com",
    "https://raw.githubusercontent.com" # Alternative Quelle
]

def transform():
    raw_data = None
    for url in SOURCES:
        try:
            print(f"Versuche Quelle: {url}")
            response = requests.get(url, headers=HEADERS, timeout=15)
            
            # Falls wir HTML statt JSON bekommen (z.B. bei 404), wirft dies einen Fehler
            if "text/html" in response.headers.get("Content-Type", ""):
                print("Warnung: Server sendete HTML statt JSON (404?).")
                continue
                
            response.raise_for_status()
            raw_data = response.json()
            print("Quelle erfolgreich geladen.")
            break 
        except Exception as e:
            print(f"Fehler bei dieser Quelle: {e}")

    if not raw_data:
        print("KRITISCH: Keine Datenquelle erreichbar.")
        sys.exit(1)

    transformed = []

    def walk(data, category="System"):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str) and "prefs:" in value:
                    transformed.append({
                        "name": key,
                        "category": category,
                        "iconName": "gearshape.fill",
                        "description": f"Direktzugriff auf {key}",
                        "urlScheme": value.replace("prefs:", "App-prefs:"),
                        "keywords": [key.lower(), category.lower(), "ios"]
                    })
                else:
                    walk(value, category=key)
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    name = item.get('title') or item.get('name') or 'Unbekannt'
                    url = item.get('url', '')
                    if "prefs:" in url:
                        transformed.append({
                            "name": name,
                            "category": category,
                            "iconName": "gearshape.fill",
                            "description": f"Direktzugriff auf {name}",
                            "urlScheme": url.replace("prefs:", "App-prefs:"),
                            "keywords": [name.lower(), "ios"]
                        })

    walk(raw_data)

    if transformed:
        with open('ecehub_master.json', 'w', encoding='utf-8') as f:
            json.dump(transformed, f, indent=2, ensure_ascii=False)
        print(f"ERFOLG: {len(transformed)} Shortcuts gespeichert.")
    else:
        print("Fehler: Keine Daten extrahiert.")
        sys.exit(1)

if __name__ == "__main__":
    transform()
