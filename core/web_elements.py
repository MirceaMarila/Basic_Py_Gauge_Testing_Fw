import time

from core.base_test import BaseTest as bt
from core.wraps import stale_element_reference, element_click_intercepted
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class WebElement:

    def __init__(self, xpath, clickable=True):
        if bt.driver.current_url[-11:] == "engagements":
            bt.finder.visible_element(['xpath', '//b[contains(text(), \"You have reached the end of the list.\")]'])

        timeout = 2
        while timeout:
            try:
                if clickable:
                    bt.finder.clickable_element(['xpath', xpath])
                else:
                    bt.finder.presence_of_element(['xpath', xpath])
                break
            except:
                timeout -= 1

        self.element = bt.driver.find_element('xpath', xpath)

    def scroll_into_view(self, highlight=True):
        try:
            bt.driver.execute_script("arguments[0].scrollIntoView();", self.element)
            if highlight:
                self.highlight(effect_time=0.2)
        except:
            pass

    def is_displayed(self):
        self.scroll_into_view()
        return self.element.is_displayed()

    def get_text(self):
        self.scroll_into_view()
        return self.element.text or self.element.get_attribute("value")

    @element_click_intercepted
    @stale_element_reference
    def click(self, double=False, highlight=True):
        self.scroll_into_view(highlight)
        try:
            if double:
                ActionChains(bt.driver).double_click(self.element).perform()
            else:
                self.element.click()

        except:
            self.click_js(highlight)

    @element_click_intercepted
    @stale_element_reference
    def click_js(self, highlight=True):
        self.scroll_into_view(highlight)
        bt.driver.execute_script(f"arguments[0].click();", self.element)

    def highlight(self, effect_time=None, color="yellow", border=3):
        def apply_style(s):
            bt.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                     self.element, s)

        try:
            original_style = self.element.get_attribute('style')
            apply_style("border: {0}px solid {1};".format(border, color))
            if effect_time:
                time.sleep(effect_time)
                apply_style(original_style)  # self.highlight(3, "red", 3)

        except:
            pass

    @element_click_intercepted
    @stale_element_reference
    def is_readonly(self):
        html_before = bt.driver.page_source
        try:
            self.click(highlight=False)
            html_after = bt.driver.page_source
            if html_before == html_after:
                return True

            else:
                html_before_second_click = bt.driver.page_source
                self.click(highlight=False)
                html_after_second_click = bt.driver.page_source

                if html_before_second_click == html_after_second_click:
                    return True

            return False

        except:
            return True

    @element_click_intercepted
    @stale_element_reference
    def is_clickable(self):
        old_url = bt.driver.current_url
        html_before = bt.driver.page_source
        result = None

        try:
            self.click(highlight=False)
            html_after = bt.driver.page_source

            if html_before == html_after:
                result = False
            else:
                result = True
                bt.driver.get(old_url)

        except:
            result = False

        finally:
            if bt.driver.current_url != old_url:
                bt.driver.back()

            return result

    def has_children(self):
        if self.element.get_attribute('innerHTML'):
            return True
        return False


class Button(WebElement):
    def __init__(self, xpath=None, text=None, value=None):
        if not xpath:
            xpath = f"//button/span[text()=\"{text}\"]/..|" \
                    f"//button/div[text()=\"{text}\"]/..|" \
                    f"//button//span[text()=\"{text}\"]|" \
                    f"//button//span//p[contains(text(), \"{text}\")]|" \
                    f"//input[@value=\"{value if value else text}\"]|" \
                    f"//a[@href]/p[contains(text(), \"{text}\")]|" \
                    f"//p[contains(text(), \"{text}\")]|" \
                    f"//li[contains(text(), \"{text}\")]|" \
                    f"//h6[contains(text(), \"{text}\")]"

        super().__init__(xpath)

    def is_enabled(self):
        return self.element.is_enabled()


class TextBox(WebElement):
    def __init__(self, xpath=None, text=None, value=None):
        if not xpath:
            xpath = f"//input[@placeholder=\"{value if value else text}\"]|" \
                    f"//input[@aria-label=\"{value if value else text}\"]|" \
                    f"//label[text()=\"{value if value else text}\"]/..//input[@type=\"number\"]|" \
                    f"//input[@name=\"{value.lower() if value else text.lower()}\"]|" \
                    f"//input[@name=\"{value if value else text}\"]|" \
                    f"//textarea[@name=\"{value.lower() if value else text.lower()}\"]|" \
                    f"//textarea[@placeholder=\"{value if value else text}\"]|" \
                    f"//textarea[@type=\"{value}\"]|" \
                    f"//textarea[@id=\"{value}\"]|" \
                    f"//textarea[@autocomplete]"

        super().__init__(xpath)

    @element_click_intercepted
    @stale_element_reference
    def write_text(self, text):
        self.scroll_into_view()
        try:
            self.clear()
            self.element.send_keys(text)

        except:
            self.write_text_js(text)

    @element_click_intercepted
    @stale_element_reference
    def append_text(self, text):
        self.scroll_into_view()
        self.element.send_keys(text)

    def clear(self):
        try:
            self.element.clear()
        except:
            pass
        self.element.send_keys(Keys.CONTROL, 'a', Keys.DELETE)

    @element_click_intercepted
    @stale_element_reference
    def write_text_js(self, text):
        self.scroll_into_view()
        bt.driver.execute_script(f"arguments[0].value = '{text}'", self.element)
        bt.logger.log_info(f"Wrote text with javascript")

    def is_read_only(self):
        readonly_bool = self.element.get_attribute("readonly")
        if not readonly_bool:
            self.write_text("text")
            readonly_bool = self.get_text() == "text"

        return readonly_bool


class TextElement(WebElement):
    def __init__(self, xpath=None, text=None, clickable=True):
        if not xpath:
            xpath = f"//div[contains(text(), \"{text}\")]|" \
                    f"//p[contains(text(), \"{text}\")]|" \
                    f"//span[contains(text(), \"{text}\")]"

        super().__init__(xpath, clickable)


class GenericElement(WebElement):
    def __init__(self, xpath=None, text=None, clickable=True):
        if not xpath:
            xpath = f"(//*[not(name()='script')][not(name()='style')][contains(text(), \"{text}\")]|" \
                    f"//*[not(name()='script')][not(name()='style')][@placeholder=\"{text}\"]|" \
                    f"//*[not(name()='script')][not(name()='style')][@value=\"{text}\"])[last()]"

        super().__init__(xpath, clickable)


class CheckBox(WebElement):
    def __init__(self, xpath=None, text=None, type="checkbox", clickable=True):
        if not xpath:
            xpath = f"//label//p[text()=\"{text}\"]/../..//input|" \
                    f"//div//label[contains(text(), \"{text}\")]/preceding::input[@type=\"{type}\"]|" \
                    f"//*[contains(text(), \"{text}\")]/../..//input[@type=\"{type}\"]"

        super().__init__(xpath, clickable=clickable)

    def is_checked(self):
        return True if self.element.get_attribute('checked') == 'true' else False

    def check(self):
        self.scroll_into_view()
        if not self.is_checked():
            self.element.click()

    def uncheck(self):
        self.scroll_into_view()
        if self.is_checked():
            self.element.click()


class InboxRow(WebElement):
    def __init__(self, text, xpath=None, tag="span", index=1):
        if not xpath:
            xpath = f"(//{tag}[contains(text(), \"{text}\")]/ancestor::tr)[{index}]"

        super().__init__(xpath)
