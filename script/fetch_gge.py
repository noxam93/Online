from datetime import datetime
import json
import os
import pytz
import requests

def fetch_data(url):
    try:
        # Udajemy narzędzie cURL, ponieważ wiemy z Twoich notatek, że cURL działa
        headers = {
            'User-Agent': 'curl/7.81.0',
            'Accept': '*/*'
        }
        
        # Timeout ustawiony na 20s w razie wybudzania serwera fly.dev
        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": f"API odrzuciło żądanie. Status: {response.status_code}",
                "szczegoly": response.text[:100]
            }
    except Exception as e:
        return {"error": f"Błąd skryptu/sieci: {str(e)}"}

if __name__ == "__main__":
    # Pozwalamy bibliotece requests zakodować nawiasy klamrowe {} samodzielnie.
    # Unikamy dzięki temu błędu Invalid command or headers wywołanego podwójnym kodowaniem.
    url_reborn = 'https://empire-api.fly.dev/EmpirefourkingdomsExGG2_3/ain/{"A10":115}'
    url_maddevils = 'https://empire-api.fly.dev/EmpirefourkingdomsExGG2_3/ain/{"A10":41343}'

    data_reborn = fetch_data(url_reborn)
    data_maddevils = fetch_data(url_maddevils)

    tracked_data = [
        {
            "name": "- ReBorN -",
            "tag": "RB",
            "aid": 115,
            "stats": data_reborn
        },
        {
            "name": "MADDEVILS",
            "tag": "MD",
            "aid": 41343,
            "stats": data_maddevils
        }
    ]

    os.makedirs("data", exist_ok=True)
    output = {
        "updated_at": datetime.now(pytz.timezone("Europe/Warsaw")).strftime("%Y-%m-%d %H:%M:%S"),
        "server": "E4K Polska 1",
        "alliances": tracked_data,
    }

    with open("data/stats.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
        
