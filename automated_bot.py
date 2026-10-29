import os.path

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import  WebDriverWait

from datetime import datetime

class AutomatedBot:
    def __init__(self, website_url):
        # initialize chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        # set up a driver to chrome
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(url=website_url)
        # set up an explicit wait
        self.wait = WebDriverWait(self.driver, timeout=5)

    def register_as_a_new_user(self, name, email, password):
        """ register as a new user """
        try:
            register_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "Home_heroButton__3eeI3")))
            register_button.click()

            self.wait.until(EC.staleness_of(register_button))
            self.driver.find_element(By.ID, "toggle-login-register").click()

            # get hold of name field and send name through
            name_placeholder = self.driver.find_element(By.NAME, "name")
            name_placeholder.send_keys(name)

            # get hold of email field and send the email through
            email_placeholder = self.driver.find_element(By.NAME, "email")
            email_placeholder.send_keys(email)

            # get hold of the password field and send the password through
            password_placeholder = self.driver.find_element(By.NAME, "password")
            password_placeholder.send_keys(password)

            # submit
            submit_button = self.driver.find_element(By.ID, "submit-button")
            submit_button.click()

            # check if either registration was successful as a new user or is there a new user already exist
            if self. wait.until(EC.any_of(EC.presence_of_element_located((By.CLASS_NAME, "Login_errorMessage__5r698")), EC.staleness_of(submit_button))):
                # if user already exist
                try:
                    self.driver.find_element(By.CLASS_NAME, "Login_errorMessage__5r698")
                    print("Already Registered, Logging in with an existing account....")
                    self.driver.find_element(By.ID, "toggle-login-register").click()
                # registration as a new user successful
                except NoSuchElementException:
                    print("Registration Successful.")
                    # logout
                    self.driver.find_element(By.ID, "logout-button").click()
                # login with the created email and password
                self.login(email, password)

        except TimeoutException:
            print("Something went wrong with the registration process.")
            self.driver.quit()

    def login(self, email, password):
        """ login using an existing email and password """
        login_button = self.wait.until(EC.element_to_be_clickable((By.ID, "login-button")))
        login_button.click()

        # get hold of email field and send the email through
        email_placeholder = self.wait.until(EC.presence_of_element_located((By.NAME, "email")))
        email_placeholder.clear()
        email_placeholder.send_keys(email)

        # get hold of the password field and send the password through

        password_placeholder = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
        password_placeholder.clear()
        password_placeholder.send_keys(password)

        # submit
        submit_button = self.driver.find_element(By.ID, "submit-button")
        submit_button.click()
        print("login Successful!")

    def book_an_upcoming_class(self, class_type, time, weekday):
        """ Book an upcoming class according to the given time and class_type"""
        # select the desired class
        try:
            select_element = self.wait.until(EC.presence_of_element_located((By.ID, "type-filter")))
            select = Select(select_element)
            select.select_by_value(class_type)

            # get all the class days
            class_days = self.driver.find_elements(By.CLASS_NAME, "Schedule_dayGroup__y79__")

            # calculate how many day to add from the current day to find the next tuesday
            weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            today_weekday = datetime.now().strftime("%A")
            today_index = weekdays.index(today_weekday)
            days_to_add = (weekdays.index(weekday.title())-today_index) % 7
            # skip if today is tuesday (because you can only book a week in advance)
            if days_to_add == 0:
                print("Reservations cannot exceed 7 days.")
                return
            # get the given day classes
            classes_for_given_day = class_days[days_to_add].find_elements(By.CLASS_NAME, "ClassCard_card__KpCx5")
            given_day_class_ids = [item.get_attribute("id") for item in classes_for_given_day]

            class_to_book = None
            # from the given day class ids loop through and figure out if it equals the given time
            for item in given_day_class_ids:
                if time == item.split("-")[-1]:
                    class_to_book = self.driver.find_element(By.ID, item)
                    break
            # if a class is found
            if class_to_book is not None:
                button = class_to_book.find_element(By.TAG_NAME, "button")

                # format class details
                class_details = class_to_book.get_attribute("data-class-id").split("-")
                date_to_format = datetime(int(class_details[1]), int(class_details[2]), int(class_details[3]))
                weekday_of_class_booked = date_to_format.strftime("%a")
                month_of_class_booked =  date_to_format.strftime("%b")
                day_of_class_booked = date_to_format.strftime("%d")

                # check if the button isn't disabled
                if not button.get_attribute("disabled"):
                    button.click()
                    # if not either join the waitlist or book the class
                    class_status = "Joined waitlist for" if class_to_book.get_attribute("data-user-waitlisted") else "Booked"
                    print(f"✓ {class_status}: {class_details[0]} Class on, "
                          f"{weekday_of_class_booked}, {month_of_class_booked}"
                          f" {day_of_class_booked}")
                # if button is disabled
                else:
                    # check if the button is disabled because it's already booked
                    if class_to_book.get_attribute("data-user-booked") != "false":
                        print(f"✓ Already booked: {class_details[0]} Class on, "
                              f"{weekday_of_class_booked}, {month_of_class_booked}"
                              f" {day_of_class_booked}")
                    # check if the button is disabled because it's already on a waitlist
                    if class_to_book.get_attribute("data-user-waitlisted") != "false":
                        print(f"✓ Already on waitlist: " 
                              f"{weekday_of_class_booked}, {month_of_class_booked}"
                              f" {day_of_class_booked}")
            # can't find any classes for the given date, time or class type
            else:
                print("No such class at that time.")

        except TimeoutException:
            print("Something went wrong when booking the class")
            self.driver.quit()

