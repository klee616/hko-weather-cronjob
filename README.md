Markdown
# 🌦️ HKO Weather Data Pipeline & Collector

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14%2B-blue)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-green)

An automated data pipeline that fetches real-time meteorological data (`rhrread` endpoint) from the **Hong Kong Observatory (HKO) Open Data API**, parses the nested JSON payloads, and ingests them into a normalized PostgreSQL database designed for **Tableau / Power BI analytics**.

---

## 📌 Features

- **Automated Ingestion**: Runs via GitHub Actions on a 5-minute cron schedule at zero infrastructure cost.
- **Deduplication Logic**: Compares API `updateTime` timestamps against the latest database record to eliminate redundant writes.
- **Normalized Schema Design**: Uses a Snapshot-Fact model (`weather_snapshots` and `fact_temperature`) to solve spatial/temporal granularity mismatches across different weather metrics.
- **Environment Driven**: Fully configured via environment variables for seamless local development and secure CI/CD cloud deployment.

---

## 🚀 Quick Start

### 1. Clone Repository & Install Dependencies

```bash
git clone [https://github.com/YOUR_USERNAME/hko-weather-collector.git](https://github.com/YOUR_USERNAME/hko-weather-collector.git)
cd hko-weather-collector
pip install -r requirements.txt
2. Configure Environment Variables (.env)
Create a .env file in the root directory (do not commit this to GitHub):

Code snippet
DB_HOST=localhost
DB_PORT=5432
DB_NAME=hko_weather
DB_USER=postgres
DB_PASSWORD=your_password
3. Run Locally
Bash
python main.py
⚙️ CI/CD & Automation (GitHub Actions)
This repository includes a workflow configuration at .github/workflows/weather_cron.yml:

Set up your repository secrets under Settings -> Secrets and variables -> Actions:

DB_HOST

DB_PORT

DB_NAME

DB_USER

DB_PASSWORD

The workflow executes automatically every 5 minutes and includes an automated keep-alive trigger to bypass GitHub's 60-day inactivity policy.

📊 Tableau Integration
Connect weather_snapshots and fact_temperature using Tableau Relationships (weather_snapshots.id = fact_temperature.snapshot_id).

Build spatial heatmaps using station coordinates or time-series dashboards to analyze temperature fluctuations across districts in Hong Kong.