import json
import requests
import sys

# Wir probieren nacheinander zwei verschiedene Quellen, falls eine offline ist
SOURCES = [
    "https://raw.githubusercontent.com",
    "https://raw.githubusercontent.com"
]

def transform():
    raw_data = None
    for url in SOURCES:
        try:
            print(f"Versuche Quelle: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            raw_data = response.json()
            print("Quelle erfolgreich geladen.")
            break 
        except Exception as e:
            print(f"Fehler bei dieser Quelle: {e}")

    if not raw_data:
        print("KRITISCH: Keine Datenquelle erreichbar oder kein JSON.")
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
                walk(item, category)

    walk(raw_data)

    if transformed:
        with open('ecehub_master.json', 'w', encoding='utf-8') as f:
            json.dump(transformed, f, indent=2, ensure_ascii=False)
        print(f"ERFOLG: {len(transformed)} Shortcuts gespeichert.")
    else:
        print("Fehler: Keine Shortcuts extrahiert.")
        sys.exit(1)

if __name__ == "__main__":
    transform()
