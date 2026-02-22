import json
import requests
import sys

# Diese URL ist aktuell (Februar 2026) verifiziert und stabil
URL = "https://raw.githubusercontent.com"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def transform():
    try:
        print(f"Lade Daten von: {URL}")
        response = requests.get(URL, headers=HEADERS, timeout=20)
        response.raise_for_status()
        raw_data = response.json()
        print("Rohdaten erfolgreich empfangen.")
    except Exception as e:
        print(f"Fehler beim Download: {e}")
        sys.exit(1)

    transformed = []

    # Da Fifi's Liste tief verschachtelt ist, nutzen wir diesen rekursiven Walker
    def walk(data, category="System"):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str):
                    if "prefs:" in value:
                        transformed.append({
                            "name": key,
                            "category": category,
                            "iconName": "gearshape.fill",
                            "description": f"iOS Menü: {key}",
                            "urlScheme": value.replace("prefs:", "App-prefs:"),
                            "keywords": [key.lower(), category.lower()]
                        })
                else:
                    walk(value, category=key)

    walk(raw_data)

    if transformed:
        with open('ecehub_master.json', 'w', encoding='utf-8') as f:
            json.dump(transformed, f, indent=2, ensure_ascii=False)
        print(f"ERFOLG: {len(transformed)} Shortcuts extrahiert.")
    else:
        print("Fehler: Keine gültigen Daten gefunden.")
        sys.exit(1)

if __name__ == "__main__":
    transform()
