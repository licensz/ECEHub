import json
import os
import sys

def transform():
    path = "fifi_repo/settings-urls-sorted.json"
    
    # 1. VERIFIZIERTE IOS 18 PFADE (PascalCase Korrektur)
    ios18_fixes = {
        "Background Sounds": "Accessibility&path=AudioVisual/BackgroundSounds",
        "Battery Health": "Battery&path=BATTERY_HEALTH",
        "Keyboards": "General&path=Keyboard",
        "Software Update": "General&path=SOFTWARE_UPDATE_LINK",
        "VoiceOver": "Accessibility&path=VoiceOver"
    }

    translations = {
        "Accessibility": "Bedienungshilfen",
        "Battery": "Batterie",
        "General": "Allgemein",
        "Background Sounds": "Hintergrundgeräusche"
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
                    display_name = translations.get(key, key)
                    if display_name == "(root)": display_name = f"{display_cat} Übersicht"
                    
                    # PFAD-LOGIK: Wir korrigieren GROSSBUCHSTABEN zu PascalCase
                    if key in ios18_fixes:
                        url = f"App-prefs:root={ios18_fixes[key]}"
                    else:
                        url = value.replace("prefs:", "App-prefs:")
                        # WICHTIG: Korrektur der Hauptkategorien für iOS 18
                        url = url.replace("root=ACCESSIBILITY", "root=Accessibility")
                        url = url.replace("root=DISPLAY", "root=Display")
                        url = url.replace("root=WIFI", "root=WIFI") # WIFI bleibt oft groß
                    
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
    print(f"SYNC ERFOLGREICH: {len(transformed)} Shortcuts für iOS 18 optimiert.")

if __name__ == "__main__": transform()
