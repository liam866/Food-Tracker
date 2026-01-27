# Food Tracker (v1)

This is v1 of a single-user food tracking application. It is designed to be a small, scoped project focusing on core functionality with a modular and scalable architecture.

## Confirmed Scope (v1)

*   Simple food logging
*   Manual food search
*   Calorie + macro tracking
*   Minimal UI

## Out of Scope

*   No AI, OCR, external APIs, cloud services, ML, background workers, or user authentication.
*   No multiple users or multi-day analytics.
*   Any features not explicitly listed in the v1 scope are intentionally excluded.

## How to Run Locally

To run this application using Docker Compose, ensure you have Docker installed on your system. Navigate to the root directory of this project and execute the following command:

```bash
docker compose up --build
```

The application will be accessible at `http://localhost:8000` in your web browser.

## API Overview (Coming in M3)

(Details about API endpoints will be added here in M3)

## Repository Structure

```
food-tracker/
├── docker-compose.yml
├── README.md
│
├── api/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── food_data.csv
│   │
│   └── app/
│       ├── main.py
│       │
│       ├── core/
│       │   ├── config.py
│       │   └── lifespan.py
│       │
│       ├── db/
│       │   ├── database.py
│       │   ├── models.py
│       │   └── init_db.py
│       │
│       ├── routes/
│       │   ├── foods.py
│       │   ├── logs.py
│       │   └── user.py
│       │
│       ├── services/
│       │   ├── food_search.py
│       │   ├── calorie_calc.py
│       │   └── food_log.py
│       │
│       └── static/
│           ├── index.html
│           ├── app.js
│           └── styles.css
```
