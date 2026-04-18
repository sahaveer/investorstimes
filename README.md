# InvestorTimes Algo

A comprehensive stock analysis dashboard built with Streamlit, MongoDB, and Selenium.

## Features
- **Fundamental Analysis**: Yearly and Quarterly P&L, Balance Sheet, and Cash Flow visualization.
- **Interactive Charts**: Dynamic Plotly figures for better data insights.
- **Stock Search**: Integrated NSE/BSE search functionality.
- **Cloud Native**: Designed to work locally (admin mode with scrapers) and on Streamlit Cloud (reader mode).
- **Telegram Integration**: Send insights and alerts directly to Telegram.

## Setup

### Local Development
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your `.streamlit/secrets.toml` with:
   - `MONGODB_URI`
   - `SCREENER_EMAIL`
   - `SCREENER_PASSWORD`
   - `TELEGRAM_TOKEN`
   - `TELEGRAM_CHAT`
4. Run the app:
   ```bash
   streamlit run main.py
   ```

### Streamlit Cloud Deployment
1. Push this repository to GitHub.
2. Connect the repository to [Streamlit Cloud](https://share.streamlit.io/).
3. Add the same secrets from your `.streamlit/secrets.toml` to the Streamlit Cloud dashboard under **Settings > Secrets**.
4. Set `IS_CLOUD = true` in the secrets.

## Tech Stack
- **Frontend**: Streamlit
- **Visualization**: Plotly
- **Database**: MongoDB
- **Scraping**: Selenium (Local only)
- **Data Source**: Screener.in, NSE, BSE
