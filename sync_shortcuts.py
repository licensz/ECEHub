import json
import requests

# Die direkte RAW-URL zur sortierten JSON von FifiTheBulldog
FIFI_RAW_URL = "https://raw.githubusercontent.com"

def transform():
    try:
        response = requests.get(FIFI_RAW_URL, timeout=15)
        response.raise_for_status()
        raw_data = response.json()
        
        transformed = []

        # Rekursive Funktion, um durch die Baumstruktur zu wandern
        def walk(data, category="Allgemein"):
            if isinstance(data, dict):
                for key, value in data.items():
                    # Wenn der Wert ein String ist, ist es ein Endpunkt (URL)
                    if isinstance(value, str):
                        if "prefs:" in value:
                            # Vereinheitlichung für Apps (App-prefs:)
                            clean_url = value.replace("prefs:", "App-prefs:")
                            transformed.append({
                                "name": key,
                                "category": category,
                                "iconName": get_icon_for_category(category),
                                "description": f"iOS Menü: {key}",
                                "urlScheme": clean_url,
                                "keywords": [key.lower(), category.lower()]
                            })
                    else:
                        # Es ist ein Unterordner, wir gehen tiefer
                        new_cat = key if key != "(root)" else category
                        walk(value, category=new_cat)

        walk(raw_data)

        with open('ecehub_master.json', 'w', encoding='utf-8') as f:
            json.dump(transformed, f, indent=2, ensure_ascii=False)
        
        print(f"ERFOLG: {len(transformed)} Shortcuts aus Fifi's Liste extrahiert.")

    except Exception as e:
        print(f"Fehler: {e}")

def get_icon_for_category(cat):
    # Einfaches Mapping für SF Symbols
    mapping = {
        "Accessibility": "accessibility",
        "Battery": "battery.100",
        "Display & Brightness": "sun.max.fill",
        "General": "gearshape.fill",
        "Wi-Fi": "wifi",
        "Privacy": "hand.raised.fill"
    }
    return mapping.get(cat, "gearshape")

if __name__ == "__main__":
    transform()
