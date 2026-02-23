import json
import os
import sys

def transform():
    # Pfad zur Quelldatei von Fifi
    path = "fifi_repo/settings-urls-sorted.json"
    
    # 1. ÜBERSETZUNGEN & KATEGORIEN (Für ein deutsches App-Interface)
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
        "Emergency SOS": "Notruf SOS"
    }

    # 2. IOS 18 PFAD-KORREKTUREN (PascalCase & Deep Links)
    # Diese Korrekturen sorgen dafür, dass wir nicht bei "Apps" landen
    ios18_fixes = {
        "Background Sounds": "Accessibility&path=AudioVisual/BackgroundSounds",
        "Battery Health": "Battery&path=BATTERY_HEALTH",
        "Software Update": "General&path=SOFTWARE_UPDATE_LINK",
        "Storage": "General&path=STORAGE_MGMT",
        "Keyboards": "General&path=Keyboard",
        "VoiceOver": "Accessibility&path=VoiceOver"
    }

    if not os.path.exists(path):
        print("Fehler: Quelldatei nicht gefunden.")
        sys.exit(1)

    with open(path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    transformed = []
    seen_urls = set()

    def walk(data, category="General"):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str) and "prefs:" in value:
                    # Namen & Kategorien bestimmen
                    display_cat = translations.get(category, category)
                    display_name = display_cat if key == "(root)" else translations.get(key, key)
                    
                    # URL GENERIERUNG (App Store Ready)
                    # Wir erzwingen 'App-prefs:' und entfernen Leerzeichen
                    url = value.replace("prefs:", "App-prefs:").replace(" ", "")
                    
                    # Manuelle Korrektur für bekannte iOS 18 Pfade
                    if key in ios18_fixes:
                        url = f"App-prefs:root={ios18_fixes[key]}"
                    else:
                        # Allgemeine Korrekturen für PascalCase (Wichtig für den Deep Link)
                        url = url.replace("root=ACCESSIBILITY", "root=Accessibility")
                        url = url.replace("root=DISPLAY", "root=Display")
                        url = url.replace("root=BATTERY_USAGE", "root=Battery")
                        url = url.replace("root=GENERAL", "root=General")

                    if url in seen_urls: continue
                    seen_urls.add(url)

                    transformed.append({
                        "name": display_name,
                        "category": display_cat,
                        "iconName": "gearshape.fill", # Standard-Icon, wird in Swift gemappt
                        "description": f"Direktzugriff auf {display_name}",
                        "urlScheme": url,
                        "keywords": [display_name.lower(), display_cat.lower()]
                    })
                else:
                    walk(value, key)

    walk(raw_data)
    
    # Speichern der ecehub_master.json
    with open('ecehub_master.json', 'w', encoding='utf-8') as f:
        json.dump(transformed, f, indent=2, ensure_ascii=False)
    
    print(f"ERFOLG: {len(transformed)} saubere Shortcuts für App Intents generiert.")

if __name__ == "__main__":
    transform()
