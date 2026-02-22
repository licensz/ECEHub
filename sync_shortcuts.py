import json
import os
import sys

def transform():
    path = "fifi_repo/settings-urls-sorted.json"
    
    # MASSIVE ÜBERSETZUNGSLISTE (Erweitere diese Liste einfach bei Bedarf)
    translations = {
        # Kategorien & Hauptmenüs
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
        "Wallet & Apple Pay": "Wallet & Apple Pay",
        "Health": "Gesundheit",
        "Journal": "Journal",
        
        # Untermenüs (Häufige Begriffe)
        "Background Sounds": "Hintergrundgeräusche",
        "Audio/Visual": "Audio & Visuell",
        "VoiceOver": "VoiceOver",
        "Zoom": "Zoom",
        "Magnifier": "Lupe",
        "Touch": "Tippen & Berühren",
        "Face ID & Passcode": "Face ID & Code",
        "Software Update": "Softwareupdate",
        "Storage": "Speicher",
        "About": "Info",
        "Language & Region": "Sprache & Region",
        "VPN & Device Management": "VPN & Geräteverwaltung",
        "Date & Time": "Datum & Uhrzeit",
        "Keyboard": "Tastatur",
        "AirDrop": "AirDrop",
        "Transfer or Reset iPhone": "iPhone übertragen/zurücksetzen"
    }

    if not os.path.exists(path):
        print(f"Fehler: Datei {path} nicht gefunden!")
        sys.exit(1)

    try:
        with open(path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
    except Exception as e:
        sys.exit(1)

    transformed = []

    def walk(data, category="System"):
        if isinstance(data, dict):
            for key, value in data.items():
                # Übersetze Kategorie und Name
                current_cat = translations.get(category, category)
                
                if isinstance(value, str):
                    if "prefs:" in value:
                        # Spezialfall (root)
                        if key == "(root)":
                            display_name = f"{current_cat} Übersicht"
                        else:
                            # Suche Übersetzung für den Namen
                            display_name = translations.get(key, key)
                        
                        clean_url = value.replace("prefs:", "App-prefs:")
                        
                        transformed.append({
                            "name": display_name,
                            "category": current_cat,
                            "iconName": get_icon(current_cat),
                            "description": f"Direktzugriff auf {display_name}",
                            "urlScheme": clean_url,
                            "keywords": [display_name.lower(), current_cat.lower()]
                        })
                else:
                    # Hier geben wir die (evtl. übersetzte) Kategorie weiter
                    walk(value, category=key)

    def get_icon(cat):
        icons = {
            "Bedienungshilfen": "accessibility", "Batterie": "battery.100",
            "Anzeige & Helligkeit": "sun.max.fill", "Allgemein": "gearshape.fill",
            "Datenschutz & Sicherheit": "hand.raised.fill", "Töne & Haptik": "speaker.wave.3.fill"
        }
        return icons.get(cat, "gearshape")

    walk(raw_data)

    with open('ecehub_master.json', 'w', encoding='utf-8') as f:
        json.dump(transformed, f, indent=2, ensure_ascii=False)
    
    print(f"ERFOLG: {len(transformed)} Shortcuts extrahiert.")

if __name__ == "__main__":
    transform()
