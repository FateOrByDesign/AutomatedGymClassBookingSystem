import os
import sys

from selenium.webdriver.common import driver_finder

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

    # bot.login("student@test.com", "password123")
    # bot.login("admin@test.com", "admin123")

    retry(lambda : bot.login(LOGIN_EMAIL, LOGIN_PASSWORD), description=bot.login.__name__, stop_execution=True)
    retry(lambda : bot.book_an_upcoming_class("all", "1800", "thursday"), description=bot.book_an_upcoming_class.__name__)
    retry(lambda : bot.book_an_upcoming_class("all", "1800", "tuesday"), description=bot.book_an_upcoming_class.__name__)
    retry(lambda : bot.book_an_upcoming_class("all", "1900", "friday"), description=bot.book_an_upcoming_class.__name__)
    retry(lambda: bot.book_an_upcoming_class("spin", "1800", "tuesday"), description=bot.book_an_upcoming_class.__name__)


        # bot.book_an_upcoming_class("spin", "1800", "tuesday")
        # bot.book_an_upcoming_class("all", "0800", "saturday")
    bot.booking_stats()
    retry(lambda : bot.verify_bookings(), description=bot.verify_bookings.__name__)


def retry(func, retries=3, description=None, stop_execution=False ):
    if description is None:
        description = func.__name__
    attempts = 0
    while retries > 0:
        try:
            attempts += 1
            func()
            break
        except RuntimeError:
                print(f"Attempt {attempts} failed, retrying {description} func...")
                retries -= 1
    else:
        print(f"All {attempts} {description} attempts failed!")
        if stop_execution:
            print(f"Cannot execute program without {description} func, Stopping program.")
            sys.exit()







if __name__ == "__main__":
    main()