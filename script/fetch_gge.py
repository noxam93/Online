from datetime import datetime
import json
import os
import pytz
import requests

ZONE_ID = "EmpirefourkingdomsExGG2_3"  #[span_4](start_span)[span_4](end_span)
ALLIANCES_TO_TRACK = [
    {"name": "- ReBorN -", "tag": "RB", "aid": 115},  #[span_5](start_span)[span_5](end_span)
    {"name": "MADDEVILS", "tag": "MD", "aid": 41343},  #[span_6](start_span)[span_6](end_span)
]

API_BASE_URL = "https://empire-api.fly.dev/v1"


def check_time_window():
  pl_tz = pytz.timezone("Europe/Warsaw")
  now = datetime.now(pl_tz)
  current_time = now.time()
  start_time = datetime.strptime("06:00", "%H:%M").time()
  end_time = datetime.strptime("23:40", "%H:%M").time()
  return start_time <= current_time <= end_time


def fetch_alliance_data(aid):
  try:
    url = f"{API_BASE_URL}/{ZONE_ID}/alliance/{aid}"
    response = requests.get(url, timeout=15)
    if response.status_code == 200:
      return response.json()
  except Exception as e:
    print(f"Błąd podczas pobierania danych dla AID {aid}: {e}")
  return None


if __name__ == "__main__":
  if not check_time_window():
    print("Poza wyznaczonym oknem czasowym (6:00 - 23:40). Pomijam pobieranie.")
    exit(0)

  print(
      "Pobieranie danych dla sojuszy ReBorN i MADDEVILS z serwera E4K Polska 1..."
  )

  tracked_data = []
  for alliance in ALLIANCES_TO_TRACK:
    data = fetch_alliance_data(alliance["aid"])
    if data:
      tracked_data.append({
          "name": alliance["name"],
          "tag": alliance["tag"],
          "aid": alliance["aid"],
          "stats": data,
      })
    else:
      tracked_data.append({
          "name": alliance["name"],
          "tag": alliance["tag"],
          "aid": alliance["aid"],
          "stats": {"error": "Brak danych z API"},
      })

  os.makedirs("data", exist_ok=True)
  output = {
      "updated_at": datetime.now(pytz.timezone("Europe/Warsaw")).strftime(
          "%Y-%m-%d %H:%M:%S"
      ),
      "server": "E4K Polska 1",
      "alliances": tracked_data,
  }

  with open("data/stats.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=4)

  print("Pomyślnie zaktualizowano plik stats.json.")
  
