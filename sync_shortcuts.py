import json
import os
import sys

def transform():
    path = "fifi_repo/settings-urls-sorted.json"
    
    # 1. VERIFIZIERTE IOS 18 PFADE (Harte Korrekturen)
    # Diese Strings sind der "Master-Key", um direkt ins Menü zu springen
    ios18_fixes = {
        "Background Sounds": "ACCESSIBILITY&path=AudioVisual/BackgroundSounds",
        "Audio/Visual": "ACCESSIBILITY&path=AudioVisual",
        "Keyboards": "General&path=Keyboard",
        "Battery Health": "BATTERY_USAGE&path=BATTERY_HEALTH",
        "VoiceOver": "ACCESSIBILITY&path=VOICEOVER_TITLE",
        "Touch": "ACCESSIBILITY&path=TOUCH_TITLE",
        "Face ID & Passcode": "TOUCHID_PASSCODE",
        "Guided Access": "ACCESSIBILITY&path=GUIDED_ACCESS_TITLE",
        "Siri": "SIRI"
    }

    # 2. ÜBERSETZUNGEN
    translations = {
        "Accessibility": "Bedienungshilfen",
        "Battery": "Batterie",
        "Display & Brightness": "Anzeige & Helligkeit",
        "General": "Allgemein",
        "Privacy": "Datenschutz & Sicherheit",
        "Background Sounds": "Hintergrundgeräusche",
        "Audio/Visual": "Audio & Visuell",
        "Guided Access": "Geführter Zugriff"
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
                    
                    # IOS 18 PFAD-KORREKTUR
                    if key in ios18_fixes:
                        clean_url = f"App-prefs:root={ios18_fixes[key]}"
                    else:
                        # Standard: Kleinschreibung forcieren, da iOS 18 das lieber mag
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
    print(f"ERFOLG: {len(transformed)} Shortcuts mit iOS 18 Fixes gespeichert.")

if __name__ == "__main__": transform()
