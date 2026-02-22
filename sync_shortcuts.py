import json
import requests
import sys

# Die direkte URL zu Fifi's sortierter Liste
FIFI_URL = "https://raw.githubusercontent.com"

def transform():
    try:
        print(f"Abruf von Fifi: {FIFI_URL}")
        response = requests.get(FIFI_URL, timeout=20)
        response.raise_for_status()
        raw_data = response.json()
        
        transformed = []

        # Rekursive Funktion, um ALLES zu finden (egal wie tief es versteckt ist)
        def walk(data, category="Allgemein"):
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, str):
                        # Wir haben einen Link gefunden!
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
                        # Es ist ein Untermenü, wir gehen tiefer
                        walk(value, category=key)

        walk(raw_data)

        if len(transformed) > 50: # Sicherheitscheck: Nur speichern wenn wir Masse haben
            with open('ecehub_master.json', 'w', encoding='utf-8') as f:
                json.dump(transformed, f, indent=2, ensure_ascii=False)
            print(f"ERFOLG: {len(transformed)} Shortcuts extrahiert!")
        else:
            print("FEHLER: Zu wenig Daten gefunden, breche ab.")
            sys.exit(1)

    except Exception as e:
        print(f"KRITISCHER FEHLER: {e}")
        sys.exit(1)

if __name__ == "__main__":
    transform()
