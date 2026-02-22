import json
import os
import sys

def transform():
    # Der Pfad zur Datei im ausgeliehenen Repo
    path = "wesley_repo/settings.json"
    
    if not os.path.exists(path):
        print(f"Fehler: Datei {path} nicht gefunden!")
        sys.exit(1)

    try:
        with open(path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        print("Datei erfolgreich von Festplatte geladen.")
    except Exception as e:
        print(f"Fehler beim Lesen: {e}")
        sys.exit(1)

    transformed = []

    def walk(data, cat="Allgemein"):
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, str) and "prefs:" in v:
                    add_item(k, v, cat)
                else: walk(v, k)
        elif isinstance(data, list):
            for i in data:
                if isinstance(i, dict):
                    name = i.get('title') or i.get('name') or "Unbekannt"
                    url = i.get('url') or ""
                    if "prefs:" in url: add_item(name, url, cat)

    def add_item(name, url, cat):
        transformed.append({
            "name": name,
            "category": cat,
            "iconName": "gearshape.fill",
            "description": f"Direktzugriff auf {name}",
            "urlScheme": url.replace("prefs:", "App-prefs:"),
            "keywords": [name.lower(), cat.lower()]
        })

    walk(raw_data)

    with open('ecehub_master.json', 'w', encoding='utf-8') as f:
        json.dump(transformed, f, indent=2, ensure_ascii=False)
    print(f"ERFOLG: {len(transformed)} Shortcuts aus Wesleys Repo extrahiert.")

if __name__ == "__main__":
    transform()
