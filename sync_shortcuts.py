import json
import os
import sys

def transform():
    path = "fifi_repo/settings-urls-sorted.json"
    
    # Übersetzungen & Pfad-Korrekturen
    translations = {"Accessibility": "Bedienungshilfen", "Battery": "Batterie", "General": "Allgemein", "Privacy": "Datenschutz & Sicherheit"}
    ios18_fixes = {
        "Background Sounds": "ACCESSIBILITY&path=AudioVisual/BackgroundSounds",
        "Battery Health": "BATTERY_USAGE&path=BATTERY_HEALTH"
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
                    display_cat = translations.get(category, category)
                    display_name = display_cat if key == "(root)" else translations.get(key, key)
                    
                    # URL Generierung ohne Leerzeichen
                    url = value.replace("prefs:", "App-prefs:").replace(" ", "")
                    if key in ios18_fixes:
                        url = f"App-prefs:root={ios18_fixes[key]}"
                    
                    if url in seen_urls: continue
                    seen_urls.add(url)

                    transformed.append({
                        "name": display_name,
                        "category": display_cat,
                        "iconName": "gearshape.fill",
                        "description": f"Öffnet {display_name}",
                        "urlScheme": url,
                        "keywords": [display_name.lower()]
                    })
                else: walk(value, key)

    walk(raw_data)
    with open('ecehub_master.json', 'w', encoding='utf-8') as f:
        json.dump(transformed, f, indent=2, ensure_ascii=False)
    print(f"ERFOLG: {len(transformed)} saubere Shortcuts gespeichert.")

if __name__ == "__main__": transform()
