from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from get_chrome_driver import GetChromeDriver


def get_chrome_driver(options=None):
    get_driver = GetChromeDriver()
    get_driver.install()

    chrome_options = webdriver.ChromeOptions()
    if options:
        for option in options:
            chrome_options.add_argument(option)

    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("window.focus();")
    driver.maximize_window()

    return driver


class ElementFinder:
    def __init__(self, driver):
        self.driver = driver
        self.web_driver_wait = WebDriverWait(driver, 5)

    def clickable_element(self, locator):
        return self.web_driver_wait.until(ec.element_to_be_clickable(locator))

    def visible_element(self, locator):
        return self.web_driver_wait.until(ec.visibility_of_element_located(locator))

    def presence_of_element(self, locator):
        return self.web_driver_wait.until(ec.presence_of_element_located(locator))

    def invisibility_of_element_located(self, locator):
        return self.web_driver_wait.until(ec.invisibility_of_element_located(locator))
