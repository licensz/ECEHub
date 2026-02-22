import json
import requests
import sys

# Wir nutzen die stabilste bekannte Quelle und einen Browser-Header
URL = "https://raw.githubusercontent.com"
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}

def transform():
    print(f"Abruf von: {URL}")
    try:
        response = requests.get(URL, headers=HEADERS, timeout=20)
        # Wenn wir HTML (Fehlerseite) bekommen, brechen wir ab und nutzen den Fallback
        if "text/html" in response.headers.get("Content-Type", ""):
            raise ValueError("Server lieferte HTML statt JSON (404)")
        
        response.raise_for_status()
        raw_data = response.json()
        print("Quelle erfolgreich geladen.")
    except Exception as e:
        print(f"Fehler beim Laden: {e}. Nutze Fallback-Daten.")
        # FALLBACK: Deine Kern-Funktionen, damit die App immer läuft
        raw_data = [
            {"title": "Hintergrundgeräusche", "url": "App-prefs:root=Accessibility&path=AUDIO_VISUAL_TITLE/BackgroundSounds"},
            {"title": "Batteriezustand", "url": "App-prefs:root=BATTERY_USAGE&path=BATTERY_HEALTH"},
            {"title": "WLAN", "url": "App-prefs:root=WIFI"},
            {"title": "Softwareupdate", "url": "App-prefs:root=General&path=SOFTWARE_UPDATE_LINK"}
        ]

    transformed = []
    
    # Rekursiver Parser, der flachklopft
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

    if transformed:
        with open('ecehub_master.json', 'w', encoding='utf-8') as f:
            json.dump(transformed, f, indent=2, ensure_ascii=False)
        print(f"ERFOLG: {len(transformed)} Einträge gespeichert.")
    else:
        sys.exit("Fehler: Keine Daten generiert.")

if __name__ == "__main__":
    transform()
