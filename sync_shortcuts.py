import json
import os
import sys

def transform():
    # 1. Pfad zur Datei im "ausgeliehenen" Fifi-Ordner
    path = "fifi_repo/settings-urls-sorted.json"
    
    # Mapping für die automatische Übersetzung der Kategorien und Namen
    translations = {
        "Accessibility": "Bedienungshilfen",
        "Battery": "Batterie",
        "Display & Brightness": "Anzeige & Helligkeit",
        "General": "Allgemein",
        "Privacy": "Datenschutz & Sicherheit",
        "Sounds & Haptics": "Töne & Haptik",
        "Control Center": "Kontrollzentrum",
        "Focus": "Fokus",
        "Screen Time": "Bildschirmzeit",
        "Wallpaper": "Hintergrundbild",
        "Siri & Search": "Siri & Suche",
        "Emergency SOS": "Notruf SOS",
        "App Store": "App Store",
        "Wallet & Apple Pay": "Wallet & Apple Pay"
    }

    if not os.path.exists(path):
        print(f"Fehler: Datei {path} nicht gefunden!")
        sys.exit(1)

    try:
        with open(path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        print("Fifi-Daten erfolgreich geladen.")
    except Exception as e:
        print(f"Fehler beim Lesen: {e}")
        sys.exit(1)

    transformed = []

    # Rekursive Funktion zum "Flachklopfen" und Übersetzen
    def walk(data, category="System"):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str) and "prefs:" in value:
                    # Übersetzung anwenden oder Original behalten
                    display_name = translations.get(key, key)
                    display_cat = translations.get(category, category)
                    
                    # Wichtig für iOS 18: Wir erzwingen 'App-prefs:'
                    clean_url = value.replace("prefs:", "App-prefs:")
                    
                    transformed.append({
                        "name": display_name,
                        "category": display_cat,
                        "iconName": get_icon(display_cat),
                        "description": f"Direktzugriff auf {display_name}",
                        "urlScheme": clean_url,
                        "keywords": [display_name.lower(), display_cat.lower(), "einstellungen"]
                    })
                else:
                    walk(value, category=key)

    def get_icon(cat):
        icons = {
            "Bedienungshilfen": "accessibility",
            "Batterie": "battery.100",
            "Anzeige & Helligkeit": "sun.max.fill",
            "Allgemein": "gearshape.fill",
            "Datenschutz & Sicherheit": "hand.raised.fill",
            "Töne & Haptik": "speaker.wave.3.fill"
        }
        return icons.get(cat, "gearshape")

    walk(raw_data)

    # Speichern der fertigen ecehub_master.json
    with open('ecehub_master.json', 'w', encoding='utf-8') as f:
        json.dump(transformed, f, indent=2, ensure_ascii=False)
    
    print(f"ERFOLG: {len(transformed)} deutsche Shortcuts extrahiert.")

if __name__ == "__main__":
    transform()
