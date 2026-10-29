import os

from automated_bot import AutomatedBot
from dotenv import load_dotenv

load_dotenv()
GYM_URL = os.getenv("GYM_URL")
LOGIN_NAME = "Sanuda"
LOGIN_EMAIL= os.getenv("LOGIN_EMAIL")
LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD")


def main():
    if not GYM_URL: raise ValueError("Something went wrong when loading the GYM_URL")
    if not LOGIN_EMAIL: raise ValueError("Something went wrong when loading the LOGIN_EMAIL")
    if not LOGIN_PASSWORD: raise ValueError("Something went wrong when loading the LOGIN_PASSWORD")

    bot = AutomatedBot(GYM_URL)
    # bot.register_as_a_new_user(LOGIN_NAME, LOGIN_EMAIL, LOGIN_PASSWORD)
    bot.login("student@test.com", "password123")
    bot.book_an_upcoming_class("all", "1800", "tuesday")
    bot.book_an_upcoming_class("all", "1800", "thursday")
    bot.booking_stats()



if __name__ == "__main__":
    main()