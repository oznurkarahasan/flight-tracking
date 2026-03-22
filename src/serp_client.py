from serpapi import GoogleSearch
from src.config import Config

class FlightRadar:
    def __init__(self):
        self.api_key = Config.SERPAPI_KEY

    def search_flights(self, origin, destination, departure_date):
        params = {
            "engine": "google_flights",
            "departure_id": origin,
            "arrival_id": destination,
            "outbound_date": departure_date,
            "currency": "TRY",
            "hl": "tr",
            "api_key": self.api_key,
            "type": "2"
        }

        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            
            flights = results.get("best_flights") or results.get("other_flights")
            
            if flights:
                return flights[0]["price"]
            return None
        except Exception as e:
            print(f"SerpApi Hatası ({origin}-{departure_date}): {e}")
            return None