import json
import os
import sys

def transform():
    # Pfad zur Datei im "ausgeliehenen" Fifi-Ordner
    path = "fifi_repo/settings-urls-sorted.json"
    
    # Mapping für die automatische Übersetzung & Kategorisierung
    translations = {
        "Accessibility": "Bedienungshilfen",
        "Battery": "Batterie",
        "Display & Brightness": "Anzeige & Helligkeit",
        "General": "Allgemein",
        "Privacy": "Datenschutz & Sicherheit",
        "Sounds & Haptics": "Töne & Haptik",
        "Background Sounds": "Hintergrundgeräusche",
        "Battery Health": "Batteriezustand",
        "Software Update": "Softwareupdate",
        "Storage": "Speicher",
        "VPN": "VPN & Netzwerk"
    }

    # Interne iOS 18 Pfad-Korrekturen (Die "Scharfschützen"-Links)
    ios18_fixes = {
        "Background Sounds": "ACCESSIBILITY&path=AudioVisual/BackgroundSounds",
        "Battery Health": "BATTERY_USAGE&path=BATTERY_HEALTH",
        "Software Update": "General&path=SOFTWARE_UPDATE_LINK",
        "Storage": "General&path=STORAGE_MGMT",
        "Keyboards": "General&path=Keyboard"
    }

    if not os.path.exists(path):
        print("Fehler: Fifi-Repo nicht gefunden.")
        sys.exit(1)

    with open(path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    transformed = []
    seen_urls = set()

    def walk(data, category="General"):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str) and "prefs:" in value:
                    # 1. Namen & Kategorien übersetzen
                    display_name = translations.get(key, key)
                    if display_name == "(root)": display_name = translations.get(category, category)
                    display_cat = translations.get(category, category)
                    
                    # 2. Pfad generieren (Intelligente Bereinigung)
                    # Wir entfernen Leerzeichen, da iOS 18 diese oft ablehnt
                    if key in ios18_fixes:
                        url = f"App-prefs:root={ios18_fixes[key]}"
                    else:
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
    print(f"AUTOMATISIERUNG: {len(transformed)} Shortcuts verarbeitet.")

if __name__ == "__main__":
    transform()
