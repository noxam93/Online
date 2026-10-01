from datetime import datetime
import json
import os
import pytz
import requests
import urllib.parse

def fetch_data(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        # Wydłużony timeout do 20 sekund na tzw. "cold start" serwera
        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            return response.json()
        else:
            # Przekazuje kod błędu (np. 403) prosto na stronę
            return {
                "error": f"API odrzuciło żądanie. Status: {response.status_code}",
                "szczegoly": response.text[:100]
            }
    except Exception as e:
        # Przekazuje błąd techniczny (np. Timeout) prosto na stronę
        return {"error": f"Błąd skryptu/sieci: {str(e)}"}

if __name__ == "__main__":
    payload_reborn = '{"A10":115}'
    payload_maddevils = '{"A10":41343}'
    
    encoded_reborn = urllib.parse.quote(payload_reborn)
    encoded_maddevils = urllib.parse.quote(payload_maddevils)

    url_reborn = f"https://empire-api.fly.dev/EmpirefourkingdomsExGG2_3/ain/{encoded_reborn}"
    url_maddevils = f"https://empire-api.fly.dev/EmpirefourkingdomsExGG2_3/ain/{encoded_maddevils}"

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
        
