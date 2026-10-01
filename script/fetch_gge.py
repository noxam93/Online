from datetime import datetime
import json
import os
import pytz
import requests

def fetch_data(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=15)
        print(f"Zapytanie do API, status: {response.status_code}")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Błąd sieciowy: {e}")
    return None

if __name__ == "__main__":
    print("Pobieranie danych ze ścieżek z aplikacji...")

    url_reborn = "https://empire-api.fly.dev/EmpirefourkingdomsExGG2_3/ain/%7B%22A10%22%3A115%7D"
    url_maddevils = "https://empire-api.fly.dev/EmpirefourkingdomsExGG2_3/ain/%7B%22A10%22%3A41343%7D"

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

    print("Zaktualizowano plik stats.json!")
    
