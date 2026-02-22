import json
import os
import sys

def transform():
    # 1. Pfad zur Datei im "ausgeliehenen" Fifi-Ordner
    path = "fifi_repo/settings-urls-sorted.json"
    
    # MASSIVE ÜBERSETZUNGSLISTE (Deutsch-Korrektur)
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
        "Wallet & Apple Pay": "Wallet & Apple Pay",
        "Background Sounds": "Hintergrundgeräusche",
        "Audio/Visual": "Audio & Visuell",
        "Keyboards": "Tastatur",
        "Battery Health": "Batteriezustand",
        "Software Update": "Softwareupdate",
        "Storage": "Speicher",
        "About": "Info",
        "Language & Region": "Sprache & Region",
        "VPN & Device Management": "VPN & Geräteverwaltung",
        "Date & Time": "Datum & Uhrzeit"
    }

    # PRÄZISIONS-FIXES FÜR IOS 18 (Damit die Deep Links direkt ins Ziel springen)
    path_fixes = {
        "Background Sounds": "ACCESSIBILITY&path=AudioVisual/BackgroundSounds",
        "Audio/Visual": "ACCESSIBILITY&path=AUDIO_VISUAL_TITLE",
        "Keyboards": "General&path=Keyboard",
        "Battery Health": "BATTERY_USAGE&path=BATTERY_HEALTH",
        "Software Update": "General&path=SOFTWARE_UPDATE_LINK",
        "VoiceOver": "ACCESSIBILITY&path=VOICEOVER_TITLE",
        "Touch": "ACCESSIBILITY&path=TOUCH_TITLE",
        "Face ID & Passcode": "TOUCHID_PASSCODE",
        "Display Zoom": "DISPLAY&path=DISPLAY_ZOOM"
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

    def walk(data, category="System"):
        if isinstance(data, dict):
            for key, value in data.items():
                current_cat = translations.get(category, category)
                
                if isinstance(value, str) and "prefs:" in value:
                    # Spezialfall (root)
                    if key == "(root)":
                        display_name = f"{current_cat} Übersicht"
                    else:
                        display_name = translations.get(key, key)
                    
                    # LOGIK FÜR IOS 18 PFAD-FIXES
                    if key in path_fixes:
                        # Nutzt den hartcodierten, funktionierenden Pfad
                        clean_url = f"App-prefs:root={path_fixes[key]}"
                    else:
                        # Standard-Umwandlung
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
                    walk(value, category=key)

    def get_icon(cat):
        icons = {
            "Bedienungshilfen": "accessibility", "Batterie": "battery.100",
            "Anzeige & Helligkeit": "sun.max.fill", "Allgemein": "gearshape.fill",
            "Datenschutz & Sicherheit": "hand.raised.fill", "Töne & Haptik": "speaker.wave.3.fill",
            "Fokus": "moon.fill", "Siri & Suche": "waveform.and.mic"
        }
        return icons.get(cat, "gearshape")

    walk(raw_data)

    with open('ecehub_master.json', 'w', encoding='utf-8') as f:
        json.dump(transformed, f, indent=2, ensure_ascii=False)
    
    print(f"ERFOLG: {len(transformed)} deutsche Shortcuts extrahiert.")

if __name__ == "__main__":
    transform()
