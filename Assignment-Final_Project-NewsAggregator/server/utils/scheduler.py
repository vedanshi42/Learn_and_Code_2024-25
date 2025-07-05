import requests
import time


def run_scheduler():
    while True:
        try:
            print("Triggering news fetch and send notifications...")
            requests.get("http://localhost:8000/fetch-news")  # update articles
            requests.post(
                "http://localhost:8000/users/notifications/send"
            )  # send notifications to users
        except Exception as e:
            print(f"Scheduler error: {e}")

        # Sleep for 3.5 hours
        time.sleep(3.5 * 60 * 60)


if __name__ == "__main__":
    run_scheduler()
