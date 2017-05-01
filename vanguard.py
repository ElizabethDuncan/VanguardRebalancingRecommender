import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


class FirefoxSession():
    def __enter__(self):
        self.driver = webdriver.Firefox()
        return self

    def __exit__(self, type, value, traceback):
        self.driver.quit()


class LoginPage():
    def __init__(self, driver):
        self.driver = driver
        self.address = 'https://investor.vanguard.com/home/'

    def load(self):
        """
        Navigate to the Personal Investor login page.
        """
        self.driver.get(self.address)

    def login(self):
        """
        Login to Vanguard Personal Investor.

        You must supply your username, password, and security question via the
        command line. This currently does not work if you have two-factor
        authentication enabled for your Vanguard account.

        A precondition of this method is that the driver's current address is
        the Personal Investor login page. Call load() to navigate to that
        page prior to invoking this method.
        """

        self._fill_in_username()
        self._fill_in_password()
        self._click_login_button()

        self._wait_for_security_question_page()
        self._answer_security_question()
        self._click_do_not_remember()
        self._click_continue_button()

    def _fill_in_username(self):
        prompt = 'Username: '
        username = input(prompt)
        username_field = self.driver.find_element_by_id('USER')
        username_field.send_keys(username)

    def _fill_in_password(self):
        prompt = 'Password: '
        password = getpass.getpass(prompt)
        password_field = self.driver.find_element_by_id('PASSWORD')
        password_field.send_keys(password)

    def _click_login_button(self):
        login_button = self.driver.find_element_by_id('login')
        login_button.click()

    def _wait_for_security_question_page(self):
        timeout_seconds = 10
        WebDriverWait(
            self.driver, timeout_seconds).until(
            expected_conditions.element_to_be_clickable(
                (By.ID, 'LoginForm:ContinueInput')))

    def _answer_security_question(self):
        security_question_field = self.driver.find_element_by_css_selector(
            '#LoginForm tbody:nth-child(1) tr:nth-child(2) td:nth-child(2)')
        security_question = security_question_field.text
        prompt = '{security_question}: '.format(
            security_question=security_question)
        answer = getpass.getpass(prompt)
        answer_field = self.driver.find_element_by_id('LoginForm:ANSWER')
        answer_field.send_keys(answer)

    def _click_do_not_remember(self):
        do_not_remember_this_computer = self.driver.find_element_by_id(
            'LoginForm:DEVICE:1')
        do_not_remember_this_computer.click()

    def _click_continue_button(self):
        continue_button = self.driver.find_element_by_id(
            'LoginForm:ContinueInput')
        continue_button.click()


def main():
    with FirefoxSession() as session:
        login_page = LoginPage(session.driver)
        login_page.load()
        login_page.login()


if __name__ == '__main__':
    main()
