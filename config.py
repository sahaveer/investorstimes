import streamlit as st
import os

def is_cloud():
    """
    Check if the application is running in Streamlit Cloud.
    """
    if "IS_CLOUD" in st.secrets:
        return st.secrets["IS_CLOUD"]
    # Fallback to checking for common cloud environment variables
    if os.environ.get("STREAMLIT_RUNTIME_ENV") == "cloud":
        return True
    # Default to local if not explicitly cloud
    return False

class Config:
    @staticmethod
    def is_cloud():
        return is_cloud()

    @staticmethod
    def get_mongodb_uri():
        if Config.is_cloud():
            return st.secrets["MONGODB_URI"]
        return st.secrets.get("MONGODB_URI", "mongodb://localhost:27017/")

    @staticmethod
    def get_screener_credentials():
        """Returns (email, password) for Screener.in"""
        # Strictly use secrets, throw error if missing
        try:
            email = st.secrets["SCREENER_EMAIL"]
            password = st.secrets["SCREENER_PASSWORD"]
            return email, password
        except KeyError as e:
            st.error(f"Missing Secret: {e}. Please add it to secrets.toml")
            return "", ""

    @staticmethod
    def get_telegram_config():
        """Returns (token, chat_name) for Telegram"""
        try:
            token = st.secrets["TELEGRAM_TOKEN"]
            chat = st.secrets["TELEGRAM_CHAT"]
            return token, chat
        except KeyError as e:
            st.error(f"Missing Secret: {e}. Please add it to secrets.toml")
            return "", ""

# Helper functions for backward compatibility
def get_mongodb_uri():
    return Config.get_mongodb_uri()
