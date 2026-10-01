from datetime import datetime
import json
import os
import pytz
import requests
import urllib.parse

def fetch_data(url):
    try:
        # Dodajemy więcej nagłówków, aby udawać normalny ruch z przeglądarki
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*'
        }
        response = requests.get(url, headers=headers, timeout=15)
        print(f"URL: {url}")
        print(f"Status z API: {response.status_code}")
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Błąd odpowiedzi: {response.text}")
    except Exception as e:
        print(f"Błąd sieciowy: {e}")
    return None

if __name__ == "__main__":
    print("Rozpoczęcie pobierania danych ze ścieżek...")

    # Zmuszamy Pythona do poprawnego zakodowania znaków specjalnych, aby uniknąć błędów URL
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
            "stats": data_reborn if data_reborn else {"error": "Brak danych z API"}
        },
        {
            "name": "MADDEVILS",
            "tag": "MD",
            "aid": 41343,
            "stats": data_maddevils if data_maddevils else {"error": "Brak danych z API"}
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

    print("Skrypt zakończył działanie. Plik stats.json został zapisany.")
    
