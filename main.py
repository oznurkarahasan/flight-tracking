from datetime import datetime, timedelta
from src.serp_client import FlightRadar
from src.storage_manager import StorageManager
from src.notifier import EmailNotifier
from src.config import Config

def get_date_list(start_date_str, end_date_str):
    start = datetime.strptime(start_date_str, "%Y-%m-%d")
    end = datetime.strptime(end_date_str, "%Y-%m-%d")
    date_list = []
    curr = start
    while curr <= end:
        date_list.append(curr.strftime("%Y-%m-%d"))
        curr += timedelta(days=1)
    return date_list

def main():
    radar = FlightRadar()
    storage = StorageManager()
    notifier = EmailNotifier()
    
    print("Uçuş takibi başlatıldı...")
    found_deals = []

    all_dates = []
    if hasattr(Config, 'DATE_RANGES'):
        for start, end in Config.DATE_RANGES:
            all_dates.extend(get_date_list(start, end))
    else:
        all_dates = Config.TARGET_DATES

    for origin in Config.ORIGINS:
        for date in all_dates:
            unique_key = f"{origin}_{Config.DESTINATION}_{date}"
            current_price = radar.search_flights(origin, Config.DESTINATION, date)
            
            if current_price:
                # Sayısal temizlik
                price_cleaned = float(''.join(filter(str.isdigit, str(current_price))))
                last_price = storage.get_last_price(unique_key)
                
                if last_price is None or price_cleaned < last_price:
                    print(f"Fırsat: {origin} | {date} | {price_cleaned} TRY")
                    found_deals.append({
                        "origin": origin,
                        "date": date,
                        "new": price_cleaned,
                        "old": last_price
                    })
                    storage.save_price(unique_key, price_cleaned)
            
    if found_deals:
        notifier.send_bulk_alert(found_deals)
    else:
        print("ℹYeni bir fiyat düşüşü yok.")

if __name__ == "__main__":
    main()