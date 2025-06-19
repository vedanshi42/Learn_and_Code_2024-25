from dotenv import load_dotenv
import os

load_dotenv()

DB_SETTINGS = {
    'host': os.getenv("DB_HOST"),
    'database': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASS")
}

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
THE_NEWS_API_KEY = os.getenv("THE_NEWS_API_KEY")

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
