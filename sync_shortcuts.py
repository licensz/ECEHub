import json
import os
import sys

def transform():
    path = "fifi_repo/settings-urls-sorted.json"
    
    # 1. PRIORITÄTS-ITEMS (Erscheinen immer ganz oben in der App)
    priority_items = [
        {
            "name": "Hintergrundgeräusche",
            "category": "Audio",
            "iconName": "ear.and.waveform",
            "url": "App-prefs:root=Accessibility&path=AudioVisual/BackgroundSounds"
        },
        {
            "name": "Bedienungshilfen Übersicht",
            "category": "System",
            "iconName": "accessibility",
            "url": "App-prefs:root=Accessibility"
        }
    ]

    if not os.path.exists(path):
        print("Fehler: Fifi-Daten nicht gefunden.")
        sys.exit(1)

    with open(path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    transformed = []
    seen_urls = set()

    # Zuerst die Favoriten hinzufügen
    for item in priority_items:
        transformed.append({
            "name": item["name"],
            "category": item["category"],
            "iconName": item["iconName"],
            "description": f"Direktzugriff auf {item['name']}",
            "urlScheme": item["url"],
            "keywords": [item["name"].lower()]
        })
        seen_urls.add(item["url"])

    # Dann den Rest von Fifi einlesen (automatisch übersetzt)
    def walk(data, category="System"):
        translations = {"Accessibility": "Bedienungshilfen", "Battery": "Batterie", "General": "Allgemein"}
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str) and "prefs:" in value:
                    url = value.replace("prefs:", "App-prefs:")
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
    print(f"ERFOLG: {len(transformed)} Shortcuts (inkl. Favoriten) gespeichert.")

if __name__ == "__main__":
    transform()
