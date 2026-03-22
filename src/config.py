import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SERPAPI_KEY = os.getenv("SERPAPI_KEY")
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    
    # İstanbul (IST/SAW), Ankara (ESB)
    ORIGINS = ["IST", "SAW", "ESB"]
    DESTINATION = "AMS"
    
    DATE_RANGES = [
        "2026-08-04", "2026-08-05",
        "2027-01-19", "2027-01-20",
        "2027-01-26", "2027-01-27"
    ]