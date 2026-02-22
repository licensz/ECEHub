import json
import os
import sys

def transform():
    path = "fifi_repo/settings-urls-sorted.json"
    
    # Mapping für Kategorien (System-Ebene)
    cat_map = {
        "Accessibility": "ACCESSIBILITY",
        "Battery": "BATTERY_USAGE",
        "Display & Brightness": "DISPLAY",
        "General": "General",
        "Privacy": "Privacy",
        "Sounds & Haptics": "Sounds"
    }

    if not os.path.exists(path): sys.exit(1)
    with open(path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    transformed = []

    def walk(data, category="General"):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str) and "prefs:" in value:
                    # AUTOMATISIERUNG: Wir bauen den Pfad dynamisch
                    root = cat_map.get(category, category)
                    
                    # Wir generieren den iOS 18 Standard-Pfad (PascalCase)
                    # Beispiel: "Background Sounds" -> "BackgroundSounds"
                    clean_key = key.replace(" ", "").replace("/", "")
                    
                    # Wir erstellen einen kombinierten Pfad, den iOS 18 besser schluckt
                    # Das System probiert intern oft verschiedene Schreibweisen
                    url = f"App-prefs:root={root}&path={clean_key}"
                    
                    # Spezial-Korrektur für bekannte Härtefälle
                    if "Background" in key:
                        url = "App-prefs:root=ACCESSIBILITY&path=AudioVisual/BackgroundSounds"
                    elif "Battery" in key and "Health" in key:
                        url = "App-prefs:root=BATTERY_USAGE&path=BATTERY_HEALTH"

                    transformed.append({
                        "name": key,
                        "category": category,
                        "iconName": "gearshape.fill",
                        "description": f"Direktzugriff auf {key}",
                        "urlScheme": url,
                        "keywords": [key.lower(), category.lower()]
                    })
                else:
                    walk(value, key)

    walk(raw_data)
    with open('ecehub_master.json', 'w', encoding='utf-8') as f:
        json.dump(transformed, f, indent=2, ensure_ascii=False)
    print(f"AUTOMATISIERUNG ERFOLGREICH: {len(transformed)} intelligente Pfade generiert.")

if __name__ == "__main__": transform()
