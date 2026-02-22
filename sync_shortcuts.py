import json
import os
import sys

def transform():
    path = "fifi_repo/settings-urls-sorted.json"
    
    # Erweiterte Übersetzung & iOS 18 Pfad-Fixes
    translations = {
        "Accessibility": "Bedienungshilfen",
        "Battery": "Batterie",
        "Display & Brightness": "Anzeige & Helligkeit",
        "General": "Allgemein",
        "Privacy": "Datenschutz & Sicherheit",
        "Background Sounds": "Hintergrundgeräusche",
        "Battery Health": "Batteriezustand",
        "Software Update": "Softwareupdate"
    }

    # Spezifische iOS 18 Pfad-Korrekturen
    ios18_fixes = {
        "Background Sounds": "ACCESSIBILITY&path=AudioVisual/BackgroundSounds",
        "Battery Health": "BATTERY_USAGE&path=BATTERY_HEALTH",
        "Software Update": "General&path=SOFTWARE_UPDATE_LINK",
        "Storage": "General&path=STORAGE_MGMT"
    }

    if not os.path.exists(path): sys.exit(1)
    with open(path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    transformed = []
    seen_urls = set()

    def walk(data, category="General"):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str) and "prefs:" in value:
                    display_name = translations.get(key, key)
                    if display_name == "(root)": display_name = translations.get(category, category)
                    display_cat = translations.get(category, category)
                    
                    # URL-Generierung
                    if key in ios18_fixes:
                        url = f"App-prefs:root={ios18_fixes[key]}"
                    else:
                        # Entfernt Leerzeichen für maximale iOS 18 Kompatibilität
                        url = value.replace("prefs:", "App-prefs:").replace(" ", "")
                    
                    if url in seen_urls: continue
                    seen_urls.add(url)

                    transformed.append({
                        "name": display_name,
                        "category": display_cat,
                        "iconName": "gearshape.fill",
                        "description": f"Direktzugriff auf {display_name}",
                        "urlScheme": url,
                        "keywords": [display_name.lower(), display_cat.lower()]
                    })
                else:
                    walk(value, key)

    walk(raw_data)
    with open('ecehub_master.json', 'w', encoding='utf-8') as f:
        json.dump(transformed, f, indent=2, ensure_ascii=False)
    print(f"ERFOLG: {len(transformed)} Shortcuts synchronisiert.")

if __name__ == "__main__":
    transform()
