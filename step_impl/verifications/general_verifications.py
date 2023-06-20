import datetime
import time
from time import sleep
import pyautogui

from getgauge.python import step
from core.wraps import stale_element_reference
from core.base_test import BaseTest as bt
from core.web_elements import Button, GenericElement, TextBox, CheckBox


@step("The page title is <title>")
def check_page_title(title):
    page_title = bt.driver.title
    timeout = 5
    while page_title == bt.driver.title and timeout:
        sleep(1)
        timeout -= 1
    bt.custom_asserts.assert_equal(title, bt.driver.title, f"The page title is \'{title}\'")


@step("<text> button is clickable")
def check_if_button_is_clickable(text):
    element = Button(text=text)
    bt.custom_asserts.assert_true(element.is_enabled(), f"\'{text}\' button is clickable", element)


@step("<text> button is not clickable")
def check_if_button_is_clickable(text):
    button = Button(text=text)
    bt.custom_asserts.assert_false(button.is_clickable(), f"\'{text}\' button is not clickable", button)


@step("The element containing the text <text> is displayed")
def check_if_element_is_displayed(text):
    element = GenericElement(text=text, clickable=False)
    timeout = 5
    while not element.is_displayed() and timeout:
        time.sleep(1)
        timeout -= 1

    bt.custom_asserts.assert_true(element.is_displayed(),
                                  f"Element with text \'{text}\' is displayed", element)


@step("The element containing the text <text> is readonly")
def check_if_element_is_readonly(text):
    element = GenericElement(text=text, clickable=False)
    bt.custom_asserts.assert_true(element.is_readonly(),
                                  f"Element with text \'{text}\' is readonly", element)


@step("The element containing the text <text> is clickable")
def check_if_element_is_clickable(text):
    element = GenericElement(text=text)
    bt.custom_asserts.assert_true(element.is_clickable(), f"Element with text \'{text}\' is clickable")


@step("The field <label> contains the text <text>")
def check_if_field_contains_text(label, text):
    textbox = GenericElement(text=label)
    field_text = textbox.get_text()
    bt.custom_asserts.assert_equal(text, field_text, f"Field with label \'{label}\' contains the text \'{text}\'",
                                   textbox)


@step("The field <label> is editable")
def check_if_field_is_readonly(label):
    textbox = TextBox(value=label)
    bt.custom_asserts.assert_true(textbox.is_read_only(), f"The field \'{label}\' is editable", textbox)
    textbox.clear()


@step("The current website url is <url>")
def check_website_url(url):
    timeout = 10
    while url != bt.driver.current_url and timeout:
        time.sleep(1)
        timeout -= 1

    bt.custom_asserts.assert_equal(url, bt.driver.current_url, f"The current website url is {url}")


@step("The checkbox <text> is checked")
def verify_if_checkbox_is_checked(text):
    checkbox = CheckBox(text=text)
    bt.custom_asserts.assert_true(checkbox.is_checked(), f"Checkbox {text} is checked", checkbox)


@step("The checkbox <text> is unchecked")
def verify_if_checkbox_is_unchecked(text):
    checkbox = CheckBox(text=text)
    bt.custom_asserts.assert_false(checkbox.is_checked(), f"Checkbox {text} is unchecked", checkbox)


@stale_element_reference
@step("The element with text <text> is displayed and it is <state>")
def check_state_of_displayed_element(text, state):
    state = state.lower()
    message = f"The element with text \'{text}\' is displayed and it is \'{state}\'"

    if state == "readonly":
        element = GenericElement(text=text, clickable=False)
        state_bool = element.is_readonly() and element.is_displayed()
        bt.custom_asserts.assert_true(state_bool, message, element)

    else:
        element = GenericElement(text=text, clickable=True)
        state_bool = element.is_displayed() and element.is_clickable()
        bt.custom_asserts.assert_true(state_bool, message, element)


@step("The <label> input field is displayed and it is clickable")
def check_if_input_field_is_displayed_and_clickable(label):
    textbox = TextBox(value=label)
    bt.custom_asserts.assert_true(textbox.is_displayed() and textbox.is_clickable(),
                                  f"The \'{label}\' input field is displayed and it is clickable", textbox)


@step("The <label> checkbox is clickable")
def check_if_checkbox_is_displayed_and_clickable(label):
    checkbox = None
    timeout = 10

    while not checkbox and timeout:
        try:
            checkbox = CheckBox(text=label, clickable=False)
        except:
            time.sleep(1)
            timeout -= 1

    bt.custom_asserts.assert_true(checkbox.is_clickable(), f"The {label} checkbox is displayed and clickable", checkbox)


@step("The table with headers <headers_list> is displayed")
def check_if_team_requests_table_contains_headers(headers_list):
    headers_list = headers_list.split(", ")
    for header in headers_list:
        element = GenericElement(xpath=f"//table//th[text()=\"{header}\"]|"
                                       f"//table//th//p[text()=\"{header}\"]", clickable=False)
        bt.custom_asserts.assert_true(element.is_displayed(),
                                      f"The table contains the header \'{header}\'", element)


@step("The <name> table with headers <headers_list> is displayed")
def check_if_team_requests_table_contains_headers(name, headers_list):
    headers_list = headers_list.split(", ")
    for header in headers_list:
        element = GenericElement(xpath=f"//p[text()=\"{name}\"]/../../..//table//th/p[text()=\"{header}\"]",
                                 clickable=False)
        bt.custom_asserts.assert_true(element.is_displayed(),
                                      f"The \'{name}\' table contains the header \'{header}\'", element)
