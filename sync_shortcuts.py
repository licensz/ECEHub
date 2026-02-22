import json
import os
import sys

def transform():
    # Pfad zur Datei im "ausgeliehenen" Ordner
    path = "fifi_repo/settings-urls-sorted.json"
    
    if not os.path.exists(path):
        print(f"Fehler: Datei {path} nicht gefunden!")
        sys.exit(1)

    try:
        with open(path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        print("Fifi-Daten erfolgreich von lokal geladen.")
    except Exception as e:
        print(f"Fehler beim Lesen: {e}")
        sys.exit(1)

    transformed = []

    def walk(data, category="System"):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str) and "prefs:" in value:
                    transformed.append({
                        "name": key,
                        "category": category,
                        "iconName": "gearshape.fill",
                        "description": f"Direktzugriff auf {key}",
                        "urlScheme": value.replace("prefs:", "App-prefs:"),
                        "keywords": [key.lower(), category.lower()]
                    })
                else:
                    walk(value, category=key)

    walk(raw_data)

    with open('ecehub_master.json', 'w', encoding='utf-8') as f:
        json.dump(transformed, f, indent=2, ensure_ascii=False)
    
    print(f"ERFOLG: {len(transformed)} Shortcuts extrahiert.")

if __name__ == "__main__":
    transform()
