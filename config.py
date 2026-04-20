import streamlit as st
import os
import datetime
import pandas as pd
from telegram import Bot

def is_cloud():
    """
    Check if the application is running in Streamlit Cloud.
    """
    if "IS_CLOUD" in st.secrets:
        val = st.secrets["IS_CLOUD"]
        if isinstance(val, str):
            return val.lower() == "true"
        return bool(val)
    if os.environ.get("STREAMLIT_RUNTIME_ENV") == "cloud":
        return True
    if "STREAMLIT_SERVER_PORT" in os.environ and os.environ.get("USER") == "appuser":
        return True
    return False

def get_recent_quarters():
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    
    if 1 <= month <= 3: # JFM -> Latest is Dec (Prev Year)
        q1 = f"{year-1}-12-31"
        q2 = f"{year-1}-09-30"
    elif 4 <= month <= 6: # AMJ -> Latest is Mar (Current Year)
        q1 = f"{year}-03-31"
        q2 = f"{year-1}-12-31"
    elif 7 <= month <= 9: # JAS -> Latest is Jun (Current Year)
        q1 = f"{year}-06-30"
        q2 = f"{year}-03-31"
    else: # OND -> Latest is Sep (Current Year)
        q1 = f"{year}-09-30"
        q2 = f"{year}-06-30"
    return q1, q2

class Config:
    @staticmethod
    def is_cloud():
        return is_cloud()

    @staticmethod
    def get_mongodb_uri():
        if "MONGODB_URI" in st.secrets:
            return st.secrets["MONGODB_URI"]
        return "mongodb://localhost:27017/"

    @staticmethod
    def get_screener_credentials():
        """Returns (email, password) for Screener.in"""
        try:
            email = st.secrets["SCREENER_EMAIL"]
            password = st.secrets["SCREENER_PASSWORD"]
            return email, password
        except KeyError:
            return "", ""

    @staticmethod
    def get_telegram_config():
        """Returns (token, chat_name, scraper_chat) for Telegram"""
        try:
            token = st.secrets["TELEGRAM_TOKEN"]
            chat = st.secrets["TELEGRAM_CHAT"]
            scraper_chat = st.secrets.get("TELEGRAM_SCRAPER_CHAT", chat)
            return token, chat, scraper_chat
        except KeyError:
            return "", "", ""

    @staticmethod
    @st.cache_resource
    def get_telegram_bot():
        token, _, _ = Config.get_telegram_config()
        if token:
            try:
                return Bot(token=token)
            except Exception as e:
                print(f"Telegram Bot Error: {e}")
        return None

    @staticmethod
    def get_driver_path(driver_type="CHROME"):
        """Returns the path to the driver from secrets or defaults."""
        key = f"{driver_type}_DRIVER_PATH"
        if key in st.secrets:
            return st.secrets[key]
        return None

    # Pre-calculate at class level for easy access
    recent_quarter_txt, last_quarter_text = get_recent_quarters()

# Helper functions for backward compatibility
def get_mongodb_uri():
    return Config.get_mongodb_uri()

# Module-level variables for backward compatibility
recent_quarter_txt = Config.recent_quarter_txt
last_quarter_text = Config.last_quarter_text
