import json
import os
import sys

def transform():
    path = "fifi_repo/settings-urls-sorted.json"
    
    # 1. HARTE IOS 18 FIXES
    ios18_fixes = {
        "Background Sounds": "ACCESSIBILITY&path=AudioVisual/BackgroundSounds",
        "Keyboards": "General&path=Keyboard",
        "Battery Health": "BATTERY_USAGE&path=BATTERY_HEALTH",
        "Software Update": "General&path=SOFTWARE_UPDATE_LINK",
        "Siri": "SIRI"
    }

    if not os.path.exists(path): sys.exit(1)
    with open(path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    transformed = []
    seen_urls = set() # Zum Entfernen von Dubletten

    def walk(data, category="System"):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str) and "prefs:" in value:
                    # 1. URL bereinigen (Sonderzeichen am Ende weg)
                    clean_url = value.split('?')[0].replace("prefs:", "App-prefs:").strip()
                    
                    # 2. Dubletten-Check
                    if clean_url in seen_urls: continue
                    seen_urls.add(clean_url)
                    
                    # 3. Pfad-Korrektur
                    if key in ios18_fixes:
                        clean_url = f"App-prefs:root={ios18_fixes[key]}"
                    
                    name = key if key != "(root)" else category
                    transformed.append({
                        "name": name,
                        "category": category,
                        "iconName": "gearshape.fill",
                        "description": f"Öffnet {name}",
                        "urlScheme": clean_url,
                        "keywords": [name.lower()]
                    })
                else: walk(value, key)

    walk(raw_data)
    with open('ecehub_master.json', 'w', encoding='utf-8') as f:
        json.dump(transformed, f, indent=2, ensure_ascii=False)
    print(f"ERFOLG: {len(transformed)} saubere Shortcuts gespeichert.")

if __name__ == "__main__": transform()
