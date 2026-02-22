import json
import requests
import os

# Die Quelle von Wesley de Groot (JSON-Format)
SOURCE_URL = "https://raw.githubusercontent.com"

def transform_data():
    try:
        response = requests.get(SOURCE_URL)
        response.raise_for_status()
        raw_data = response.json()
        
        transformed = []
        
        # Rekursive Funktion, um durch die verschachtelte Struktur zu wandern
        def parse_item(name, value, category="Allgemein"):
            if isinstance(value, str):
                # Wir nehmen nur funktionierende Pfade (prefs: oder App-prefs:)
                if "prefs:" in value:
                    transformed.append({
                        "name": name,
                        "category": category,
                        "iconName": get_icon(name, category),
                        "description": f"Direktzugriff auf {name}",
                        "urlScheme": value.replace("prefs:", "App-prefs:"),
                        "keywords": [name.lower(), category.lower(), "ios", "settings"]
                    })
            elif isinstance(value, dict):
                # Wenn es ein Untermenü ist, tiefer graben
                new_cat = name if name != "(root)" else category
                for sub_name, sub_value in value.items():
                    parse_item(sub_name, sub_value, new_cat)

        for key, val in raw_data.items():
            parse_item(key, val)

        # Ergebnis speichern
        with open('ecehub_master.json', 'w', encoding='utf-8') as f:
            json.dump(transformed, f, indent=2, ensure_ascii=False)
        
        print(f"Erfolg: {len(transformed)} Einträge synchronisiert.")

    except Exception as e:
        print(f"Fehler: {e}")
        exit(1)

def get_icon(name, category):
    # Logik für automatische Icon-Zuweisung (SF Symbols)
    mapping = {
        "Batterie": "battery.100",
        "WLAN": "wifi",
        "Bluetooth": "bolt.horizontal.fill",
        "Hintergrundgeräusche": "ear.and.waveform",
        "Display": "sun.max",
        "Audio": "speaker.wave.2"
    }
    return mapping.get(name, mapping.get(category, "gearshape.fill"))

if __name__ == "__main__":
    transform_data()
