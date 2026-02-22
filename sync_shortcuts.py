import json
import os
import sys

def transform():
    path = "fifi_repo/settings-urls-sorted.json"
    
    # 1. Manuelle Korrekturen für iOS 18 (Damit Deep Links funktionieren)
    ios18_fixes = {
        "Background Sounds": "ACCESSIBILITY&path=AudioVisual/BackgroundSounds",
        "Triple-click": "ACCESSIBILITY&path=ACCESSIBILITY_SHORTCUT_TITLE",
        "Keyboards": "General&path=Keyboard",
        "Battery Health": "BATTERY_USAGE&path=BATTERY_HEALTH",
        "VoiceOver": "ACCESSIBILITY&path=VOICEOVER_TITLE",
        "Touch": "ACCESSIBILITY&path=TOUCH_TITLE",
        "Display Zoom": "DISPLAY&path=DISPLAY_ZOOM",
        "Software Update": "General&path=SOFTWARE_UPDATE_LINK"
    }

    # 2. Übersetzungen für die App
    translations = {
        "Accessibility": "Bedienungshilfen",
        "Battery": "Batterie",
        "Display & Brightness": "Anzeige & Helligkeit",
        "General": "Allgemein",
        "Privacy": "Datenschutz & Sicherheit",
        "Background Sounds": "Hintergrundgeräusche",
        "Triple-click": "Kurzbefehl"
    }

    if not os.path.exists(path): sys.exit(1)

    with open(path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    transformed = []

    def walk(data, category="System"):
        if isinstance(data, dict):
            for key, value in data.items():
                current_cat = translations.get(category, category)
                if isinstance(value, str) and "prefs:" in value:
                    display_name = f"{current_cat} Übersicht" if key == "(root)" else translations.get(key, key)
                    
                    # Hier greift die Korrektur-Logik
                    if key in ios18_fixes:
                        clean_url = f"App-prefs:root={ios18_fixes[key]}"
                    else:
                        clean_url = value.replace("prefs:", "App-prefs:")
                    
                    transformed.append({
                        "name": display_name,
                        "category": current_cat,
                        "iconName": "gearshape.fill",
                        "description": f"Öffnet {display_name}",
                        "urlScheme": clean_url,
                        "keywords": [display_name.lower(), current_cat.lower()]
                    })
                else: walk(value, category=key)

    walk(raw_data)
    with open('ecehub_master.json', 'w', encoding='utf-8') as f:
        json.dump(transformed, f, indent=2, ensure_ascii=False)
    print(f"ERFOLG: {len(transformed)} Shortcuts mit Fixes gespeichert.")

if __name__ == "__main__": transform()
