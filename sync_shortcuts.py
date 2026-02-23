import json
import os
import sys

def transform():
    path = "fifi_repo/settings-urls-sorted.json"
    
    # 1. MANUELLE PRIORITÄTEN (Damit WLAN & Co. ganz oben stehen und funktionieren)
    priority_items = [
        {
            "name": "WLAN",
            "category": "Netzwerk",
            "iconName": "wifi",
            "urlScheme": "App-prefs:root=WIFI"
        },
        {
            "name": "Batteriezustand",
            "category": "Batterie",
            "iconName": "battery.100",
            "urlScheme": "App-prefs:root=Battery&path=BATTERY_HEALTH"
        },
        {
            "name": "Hintergrundgeräusche",
            "category": "Bedienungshilfen",
            "iconName": "ear.and.waveform",
            "urlScheme": "App-prefs:root=Accessibility&path=AudioVisual/BackgroundSounds"
        },
        {
            "name": "Softwareupdate",
            "category": "Allgemein",
            "iconName": "arrow.clockwise.circle",
            "urlScheme": "App-prefs:root=General&path=SOFTWARE_UPDATE_LINK"
        }
    ]

    if not os.path.exists(path):
        print("Fehler: Quelldatei nicht gefunden.")
        sys.exit(1)

    with open(path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    transformed = []
    seen_urls = set()

    # Zuerst die Prioritäts-Items hinzufügen
    for item in priority_items:
        transformed.append({
            "name": item["name"],
            "category": item["category"],
            "iconName": item["iconName"],
            "description": f"Direktzugriff auf {item['name']}",
            "urlScheme": item["urlScheme"],
            "keywords": [item["name"].lower()]
        })
        seen_urls.add(item["urlScheme"])

    # Dann den Rest von Fifi einlesen (automatisch bereinigt)
    def walk(data, category="General"):
        translations = {"Accessibility": "Bedienungshilfen", "Battery": "Batterie", "General": "Allgemein", "Display & Brightness": "Anzeige"}
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str) and "prefs:" in value:
                    # URL säubern für App Intents / Kopieren
                    url = value.replace("prefs:", "App-prefs:").replace(" ", "")
                    if url in seen_urls: continue
                    seen_urls.add(url)
                    
                    display_cat = translations.get(category, category)
                    display_name = display_cat if key == "(root)" else key
                    
                    transformed.append({
                        "name": display_name,
                        "category": display_cat,
                        "iconName": "gearshape.fill",
                        "description": f"Öffnet {display_name}",
                        "urlScheme": url,
                        "keywords": [display_name.lower()]
                    })
                else:
                    walk(value, key)

    walk(raw_data)
    
    with open('ecehub_master.json', 'w', encoding='utf-8') as f:
        json.dump(transformed, f, indent=2, ensure_ascii=False)
    print(f"ERFOLG: {len(transformed)} Shortcuts inkl. WLAN generiert.")

if __name__ == "__main__":
    transform()
