import streamlit as st
import os

def is_cloud():
    """
    Check if the application is running in Streamlit Cloud.
    """
    # 1. Check st.secrets first
    if "IS_CLOUD" in st.secrets:
        val = st.secrets["IS_CLOUD"]
        if isinstance(val, str):
            return val.lower() == "true"
        return bool(val)
    
    # 2. Check environment variables (Streamlit Cloud sets some specific ones)
    if os.environ.get("STREAMLIT_RUNTIME_ENV") == "cloud":
        return True
    
    # 3. Fallback: check for a common cloud-only path or variable
    if "STREAMLIT_SERVER_PORT" in os.environ and os.environ.get("USER") == "appuser":
        return True
        
    return False

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
        except KeyError as e:
            # On cloud, this should be set in Secrets tab.
            # Local, it should be in .streamlit/secrets.toml
            return "", ""

    @staticmethod
    def get_telegram_config():
        """Returns (token, chat_name, scraper_chat) for Telegram"""
        try:
            token = st.secrets["TELEGRAM_TOKEN"]
            chat = st.secrets["TELEGRAM_CHAT"]
            scraper_chat = st.secrets.get("TELEGRAM_SCRAPER_CHAT", chat)
            return token, chat, scraper_chat
        except KeyError as e:
            return "", "", ""

    @staticmethod
    def get_driver_path(driver_type="CHROME"):
        """Returns the path to the driver from secrets or defaults."""
        key = f"{driver_type}_DRIVER_PATH"
        if key in st.secrets:
            return st.secrets[key]
        return None

# Helper functions for backward compatibility
def get_mongodb_uri():
    return Config.get_mongodb_uri()
