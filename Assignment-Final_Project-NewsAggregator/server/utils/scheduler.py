import os
import time
import requests
from datetime import datetime


class ClientScheduler:
    FETCH_URL = "http://localhost:8000/fetch-news"
    EMAIL_URL = "http://localhost:8000/send-notifications"
    INTERVAL_SECONDS = 3.5 * 3600
    LOG_DIR = "client/logs/server_logs"

    def __init__(self):
        os.makedirs(self.LOG_DIR, exist_ok=True)

    def log(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file = os.path.join(self.LOG_DIR, f"log_{timestamp}.txt")
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")

    def fetch_news_from_server(self):
        try:
            res = requests.get(self.FETCH_URL)
            res.raise_for_status()
            articles = res.json().get("articles", [])
            log_msg = f"{len(articles)} articles fetched successfully."
            print(log_msg)
            self.log(log_msg)
        except Exception as e:
            err = f"Error fetching news: {e}"
            print(err)
            self.log(err)

    def send_email_alerts(self):
        try:
            res = requests.post(self.EMAIL_URL)
            res.raise_for_status()
            msg = "Email notifications sent to all users."
            print(msg)
            self.log(msg)
        except Exception as e:
            err = f"Error sending emails: {e}"
            print(err)
            self.log(err)

    def run(self):
        while True:
            self.log("Scheduler cycle started.")
            self.fetch_news_from_server()
            self.send_email_alerts()
            self.log("Scheduler cycle completed. Sleeping now...\n")
            time.sleep(self.INTERVAL_SECONDS)


if __name__ == "__main__":
    ClientScheduler().run()
