import json
import os
import sys

def transform():
    # Quelle: Fifi's lokale Kopie im Repo
    path = "fifi_repo/settings-urls-sorted.json"
    
    # 1. MANUELLE ÜBERSETZUNG & IOS 18 PFAD-FIXES
    # Wir definieren hier die "Helden-Shortcuts", die JEDER braucht
    priority_items = [
        {"n": "Hintergrundgeräusche", "u": "App-prefs:root=ACCESSIBILITY&path=AudioVisual/BackgroundSounds", "c": "Audio"},
        {"n": "Batteriezustand", "u": "App-prefs:root=BATTERY_USAGE&path=BATTERY_HEALTH", "c": "Energie"},
        {"n": "Softwareupdate", "u": "App-prefs:root=General&path=SOFTWARE_UPDATE_LINK", "c": "System"},
        {"n": "WLAN", "u": "App-prefs:root=WIFI", "c": "Netzwerk"},
        {"n": "Tastatur", "u": "App-prefs:root=General&path=Keyboard", "c": "System"}
    ]

    if not os.path.exists(path): sys.exit(1)
    with open(path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    transformed = []
    seen_urls = set()

    # Zuerst die Prioritäts-Items hinzufügen
    for item in priority_items:
        transformed.append({
            "name": item["n"], "category": item["c"], "iconName": "star.fill",
            "description": f"Direktzugriff auf {item['n']}",
            "urlScheme": item["u"], "keywords": [item["n"].lower()]
        })
        seen_urls.add(item["u"])

    # Dann den Rest von Fifi einlesen (automatisch übersetzt)
    def walk(data, category="System"):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str) and "prefs:" in value:
                    url = value.replace("prefs:", "App-prefs:")
                    if url in seen_urls: continue
                    seen_urls.add(url)
                    
                    name = key if key != "(root)" else category
                    transformed.append({
                        "name": name, "category": category, "iconName": "gearshape.fill",
                        "description": f"Öffnet {name}", "urlScheme": url, "keywords": [name.lower()]
                    })
                else: walk(value, key)

    walk(raw_data)
    with open('ecehub_master.json', 'w', encoding='utf-8') as f:
        json.dump(transformed, f, indent=2, ensure_ascii=False)
    print(f"ERFOLG: {len(transformed)} Shortcuts (inkl. iOS 18 Fixes) gespeichert.")

if __name__ == "__main__": transform()
