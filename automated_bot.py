import os.path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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
        register_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "Home_heroButton__3eeI3")))
        register_button.click()
        try:
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
            try:
                if self.wait.until(EC.staleness_of(submit_button)):
                    print("Registration Successful.")
            except TimeoutException:
                print("Something went wrong registration process.")
                self.driver.quit()
        except TimeoutException:
            print("Something went wrong registration process.")
            self.driver.quit()
