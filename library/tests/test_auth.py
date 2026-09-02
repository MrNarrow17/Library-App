import time

from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

User = get_user_model()

WAIT_TIME = 5

IS_DEMO = True
DEMO_DELAY = 2


class LoginLogoutSystemTest(StaticLiveServerTestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(3)

        self.email = "testuser@gmail.com"
        self.password = "coolpassword123"

        self.user = User.objects.create_user(email=self.email, password=self.password)
        self.user.set_password(self.password)
        self.user.save()

    def tearDown(self):
        self.driver.quit()

    def demo_wait(self):
        time.sleep(DEMO_DELAY) if IS_DEMO else None

    def test_login_logout_workflow(self):
        self.driver.get(self.live_server_url)
        self.demo_wait()

        login_button = WebDriverWait(self.driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-auth-login"))
        )

        self.assertTrue(login_button.is_displayed())
        login_button.click()
        self.demo_wait()

        login_form = WebDriverWait(self.driver, WAIT_TIME).until(
            EC.visibility_of_element_located((By.TAG_NAME, "form"))
        )

        email_input = login_form.find_element(By.NAME, "email")
        password_input = login_form.find_element(By.NAME, "password")

        email_input.send_keys(self.email)
        password_input.send_keys(self.password)
        self.demo_wait()

        login_submit_button = login_form.find_element(By.CLASS_NAME, "btn-auth-login")

        self.assertTrue(login_submit_button.is_displayed())
        login_submit_button.click()
        self.demo_wait()

        logout_button = WebDriverWait(self.driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-auth-logout"))
        )
        self.assertTrue(logout_button.is_displayed())
        self.demo_wait()

        logout_button.click()
        self.demo_wait()

        login_button = WebDriverWait(self.driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-auth-login"))
        )
        self.assertTrue(login_button.is_displayed())
        self.demo_wait()

        login_button.click()
        self.demo_wait()

        login_form = WebDriverWait(self.driver, WAIT_TIME).until(
            EC.visibility_of_element_located((By.TAG_NAME, "form"))
        )

        email_input = login_form.find_element(By.NAME, "email")
        password_input = login_form.find_element(By.NAME, "password")

        email_input.send_keys("notvalidemail@gmail.com")
        password_input.send_keys("1234")
        self.demo_wait()

        login_submit_button = login_form.find_element(By.CLASS_NAME, "btn-auth-login")
        self.assertTrue(login_submit_button.is_displayed())
        login_submit_button.click()
        self.demo_wait()

        error_element = WebDriverWait(self.driver, WAIT_TIME).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "text-danger"))
        )
        self.assertTrue(error_element.is_displayed())
        self.assertIn("Invalid", error_element.text)
        self.assertFalse(self.driver.find_elements(By.CSS_SELECTOR, ".btn-auth-logout"))
        self.demo_wait()
