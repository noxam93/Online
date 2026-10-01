from datetime import datetime
import json
import os
import pytz
import http.client

def fetch_data(aid):
    # Używamy niskopoziomowego połączenia, które nie ingeruje w kodowanie znaków
    conn = http.client.HTTPSConnection("empire-api.fly.dev", timeout=20)
    
    # Dokładna, surowa ścieżka. http.client przekaże ją dokładnie w takiej formie.
    path = f"/EmpirefourkingdomsExGG2_3/ain/%7B%22A10%22%3A{aid}%7D"
    
    try:
        conn.request("GET", path, headers={"User-Agent": "Mozilla/5.0"})
        res = conn.getresponse()
        data = res.read().decode('utf-8')
        
        if res.status == 200:
            return json.loads(data)
        else:
            return {"error": f"Odrzucono. Status: {res.status}", "szczegoly": data[:100]}
    except Exception as e:
        return {"error": f"Błąd: {str(e)}"}
    finally:
        conn.close()

if __name__ == "__main__":
    data_reborn = fetch_data(115)
    data_maddevils = fetch_data(41343)

    tracked_data = [
        {"name": "- ReBorN -", "tag": "RB", "aid": 115, "stats": data_reborn},
        {"name": "MADDEVILS", "tag": "MD", "aid": 41343, "stats": data_maddevils}
    ]

    os.makedirs("data", exist_ok=True)
    output = {
        "updated_at": datetime.now(pytz.timezone("Europe/Warsaw")).strftime("%Y-%m-%d %H:%M:%S"),
        "server": "E4K Polska 1",
        "alliances": tracked_data,
    }

    with open("data/stats.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
        
