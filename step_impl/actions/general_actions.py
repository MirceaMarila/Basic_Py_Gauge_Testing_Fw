import time
import pyautogui
from getgauge.python import step
from core.wraps import stale_element_reference
from core.base_test import BaseTest as bt
from core.web_elements import Button, TextBox, CheckBox, GenericElement


@step("Access the website <website>")
def access_website(website):
    bt.driver.get(website)
    bt.driver.switch_to.window(bt.driver.current_window_handle)
    bt.logger.log_info(f"Accessed the website \'{website}\'")


@stale_element_reference
@step("Click on <text> button")
def click_on_button_by_text(text):
    Button(text=text).click()
    bt.logger.log_info(f"Clicked on \'{text}\' button")


@stale_element_reference
@step("Double click on <text> button")
def double_click_on_button_by_text(text):
    Button(text=text).click(double=True)
    bt.logger.log_info(f"Double clicked on \'{text}\' button")


@step("Fill in the <label> textbox with the text <text> and submit")
def fill_in_textbox_with_text(label, text):
    textbox = TextBox(value=label)
    message = ""

    textbox.write_text(text)
    textbox.element.submit()
    bt.logger.log_info(f"Wrote \'{text}\' in the \'{label}\' textbox" + message)


@step("Focus on tab number <nr>")
def focus_on_tab_nr(nr):
    bt.driver.switch_to.window(bt.driver.window_handles[int(nr)-1])
    bt.logger.log_info(f"Focus changed on tab number {nr}")


@step("Refresh webpage")
def refresh_webpage():
    bt.driver.refresh()
    bt.logger.log_info("Page refreshed")


@step("Wait <nr> seconds")
def wait_seconds(nr):
    bt.logger.log_info(f"Waiting \'{nr}\' seconds...")
    time.sleep(int(nr))


@stale_element_reference
@step("Check the <text> checkbox")
def check_checkbox(text):
    checkbox = CheckBox(text=text, clickable=False)
    checkbox.check()
    bt.logger.log_info(f"Checked the \'{text}\' checkbox")


@step("Uncheck the <text> checkbox")
def uncheck_checkbox(text):
    CheckBox(text=text).uncheck()
    bt.logger.log_info(f"Unchecked the \'{text}\' checkbox")


@step("Go back")
def go_back():
    bt.driver.back()
    bt.logger.log_info("Went on the previous page")


@step("Go back to <url>")
def go_back_to_url(url):
    if bt.driver.current_url != url:
        bt.driver.back()

        if bt.driver.current_url != url:
            bt.driver.get(url)

    bt.logger.log_info(f"Went back to \'{url}\'")


@step("Press <key>")
def press_key(key):
    pyautogui.press(key.lower())
    bt.logger.log_info(f"{key} button pressed")


@step("Click on element with text <text>")
def click_on_element_with_text(text):
    GenericElement(text=text, clickable=False).click()
    bt.logger.log_info(f"Clicked on element with text \'{text}\'")


@step("Click on <text> checkbox")
def click_on_checkbox(text):
    CheckBox(text=text, clickable=False).click()
    bt.logger.log_info(f"Clicked on \'{text}\' checkbox")
