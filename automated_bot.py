import os.path

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.support.wait import  WebDriverWait

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

            if self. wait.until(EC.any_of(EC.presence_of_element_located((By.CLASS_NAME, "Login_errorMessage__5r698")), EC.staleness_of(submit_button))):
                try:
                    self.driver.find_element(By.CLASS_NAME, "Login_errorMessage__5r698")
                    print("Already Registered, Logging in with an existing account....")
                    self.driver.find_element(By.ID, "toggle-login-register").click()
                except NoSuchElementException:
                    print("Registration Successful.")
                    # logout
                    self.driver.find_element(By.ID, "logout-button").click()
                # login with the created email and password
                self.login(email, password)


        except TimeoutException:
            print("Something went wrong with the registration process.")
            # self.driver.quit()

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


