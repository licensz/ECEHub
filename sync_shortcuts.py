import json
import os
import sys

def transform():
    path = "fifi_repo/settings-urls-sorted.json"
    
    # DIE GOLDENEN PFADE FÜR IOS 18
    # Wir überschreiben hier die alten Fifi-Pfade mit verifizierten iOS 18 Strings
    ios18_fixes = {
        "Background Sounds": "Accessibility&path=AudioVisual/BackgroundSounds",
        "Battery Health": "BATTERY_USAGE&path=BATTERY_HEALTH",
        "Keyboards": "General&path=Keyboard",
        "Software Update": "General&path=SOFTWARE_UPDATE_LINK",
        "Siri": "SIRI",
        "VoiceOver": "Accessibility&path=VOICEOVER_TITLE"
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
                    
                    # PFAD-LOGIK
                    if key in ios18_fixes:
                        url = f"App-prefs:root={ios18_fixes[key]}"
                    else:
                        # Standard: Wir machen aus 'ACCESSIBILITY' -> 'Accessibility'
                        url = value.replace("prefs:root=ACCESSIBILITY", "App-prefs:root=Accessibility")
                        url = url.replace("prefs:", "App-prefs:")
                    
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
    print(f"ERFOLG: {len(transformed)} Shortcuts für iOS 18 optimiert.")

if __name__ == "__main__": transform()
