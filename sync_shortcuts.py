import json
import sys

# Wir betten die stabilsten Pfade direkt ein, um 404-Fehler zu vermeiden
RAW_DATA = {
    "Bedienungshilfen": {
        "Hintergrundgeräusche": "App-prefs:root=Accessibility&path=AUDIO_VISUAL_TITLE/BackgroundSounds",
        "Hörhilfen": "App-prefs:root=Accessibility&path=HEARING_AID_TITLE",
        "Untertitel": "App-prefs:root=Accessibility&path=SUBTITLES_CAPTIONING",
        "Lupe": "App-prefs:root=Magnifier"
    },
    "Batterie": {
        "Batteriezustand": "App-prefs:root=BATTERY_USAGE&path=BATTERY_HEALTH",
        "Stromsparmodus": "App-prefs:root=BATTERY_USAGE"
    },
    "Anzeige": {
        "Helligkeit": "App-prefs:root=DISPLAY",
        "Auto-Sperre": "App-prefs:root=DISPLAY&path=AUTOLOCK",
        "Textgröße": "App-prefs:root=DISPLAY&path=TEXT_SIZE"
    },
    "System": {
        "Softwareupdate": "App-prefs:root=General&path=SOFTWARE_UPDATE_LINK",
        "Speicher": "App-prefs:root=General&path=STORAGE_MGMT",
        "Info": "App-prefs:root=General&path=About",
        "VPN": "App-prefs:root=General&path=VPN",
        "WLAN": "App-prefs:root=WIFI",
        "Bluetooth": "App-prefs:root=Bluetooth"
    }
}

def transform():
    transformed = []
    
    for category, items in RAW_DATA.items():
        for name, url in items.items():
            transformed.append({
                "name": name,
                "category": category,
                "iconName": "gearshape.fill",
                "description": f"Direktzugriff auf {name}",
                "urlScheme": url,
                "keywords": [name.lower(), category.lower(), "ios"]
            })
    
    # Hier könntest du später weitere Pfade per Skript hinzufügen
    with open('ecehub_master.json', 'w', encoding='utf-8') as f:
        json.dump(transformed, f, indent=2, ensure_ascii=False)
    
    print(f"ERFOLG: {len(transformed)} Shortcuts in ecehub_master.json gespeichert.")

if __name__ == "__main__":
    transform()
