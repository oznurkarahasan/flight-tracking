# Flight Tracking

A lightweight Python project that monitors flight prices, stores the latest known prices, and sends an email alert when a lower price is found.

By default, it monitors flights from `IST`, `SAW`, and `ESB` to `AMS`.
You can change both origin and destination airports in `src/config.py` by editing `ORIGINS` and `DESTINATION`.

## What this project does

- Queries flight prices using SerpApi (`google_flights` engine)
- Tracks routes from multiple origin airports to one destination
- Checks specific travel dates (or date ranges)
- Saves historical prices in `data/price_history.json`
- Sends a summary email when new price drops are detected
- Can run manually, in Docker, or on a GitHub Actions schedule (Monday and Thursday)

## Project structure

```text
flight-tracking/
├── main.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── data/
│   └── price_history.json
└── src/
    ├── config.py
    ├── serp_client.py
    ├── storage_manager.py
    └── notifier.py
```

## How it works

1. `main.py` builds a list of dates from `Config.DATE_RANGES`.
2. For each origin/date pair, `FlightRadar` requests current prices from SerpApi.
3. The app compares the new price with the stored price in `price_history.json`.
4. If the new price is lower (or first record), it updates storage.
5. If at least one drop is found, `EmailNotifier` sends a bulk summary email.

## Configuration

Edit `src/config.py` to customize:

- `ORIGINS` (departure airports, e.g., `IST`, `SAW`, `ESB`)
- `DESTINATION` (arrival airport, e.g., `AMS`)
- `DATE_RANGES` (date list or date tuples)

Environment variables are loaded with `python-dotenv`:

- `SERPAPI_KEY`
- `EMAIL_ADDRESS`
- `EMAIL_PASSWORD`

Create a `.env` file in the project root:

```env
SERPAPI_KEY=your_serpapi_key
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

## Run locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

## Run with Docker

Build an image from `Dockerfile` and run it:

```bash
docker build -t flight-tracking:latest .
docker run --rm --env-file .env -v "$(pwd)/data:/app/data" flight-tracking:latest
```

Or use Docker Compose:

```bash
docker compose up --build
```

## GitHub Actions automation

The workflow in `.github/workflows/monitor.yml`:

- checks dates only on Monday and Thursday,
- installs dependencies,
- runs `python3 main.py`,
- commits updated `data/price_history.json` back to the repository.

Required repository secrets:

- `SERPAPI_KEY`
- `EMAIL_ADDRESS`
- `EMAIL_PASSWORD`

## Notes

- For Gmail, use an App Password (not your normal account password).
- Price parsing currently extracts numeric characters and stores values as float.
- Notifications are sent only when a lower price is detected.
