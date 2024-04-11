import time

import win32con
import win32gui
from getgauge.python import before_scenario, after_scenario, after_spec, ExecutionContext, after_step
from core.custom_asserts import CustomAsserts
from core.logger import Logger
from core.utils import get_the_nr_of_steps_in_scenario, focus_on_driver_window
from core.json_methods import get_run_setting, get_spec_property, set_spec_property, get_test_utils, set_test_utils, \
    save_result_to_json
from core.web_driver import get_chrome_driver, ElementFinder
import pyautogui
from win10toast import ToastNotifier
from core.settings import BASE_PATH


class BaseTest:
    driver: None
    finder: ElementFinder = None
    custom_asserts: CustomAsserts = None
    logger: Logger = None
    current_ide = win32gui.GetForegroundWindow()


@before_scenario
def before_scenario(context: ExecutionContext):
    pyautogui.FAILSAFE = False
    BaseTest.driver = get_chrome_driver(options=['--incognito'])
    focus_on_driver_window()

    BaseTest.finder = ElementFinder(BaseTest.driver)
    BaseTest.logger = Logger(context.scenario.name, context.specification.file_name)
    BaseTest.custom_asserts = CustomAsserts(BaseTest.logger)
    set_test_utils("driver_pid", BaseTest.driver.service.process.pid)
    set_test_utils("steps", 0)

    try:
        toast = ToastNotifier()
        toast.show_toast(
            f"{context.specification.name}",
            f"{context.scenario.name}",
            duration=25,
            icon_path=f"{BASE_PATH}\\reports\\html-report\\images\\favicon.ico",
            threaded=True,
        )

    except:
        pass


@after_scenario
def after_scenario(context: ExecutionContext):
    win32gui.ShowWindow(BaseTest.current_ide, win32con.SW_MAXIMIZE)
    nr_of_steps = get_the_nr_of_steps_in_scenario(context.specification.file_name, context.scenario.name)
    result = 'FAIL' if any(BaseTest.custom_asserts.failed_asserts) or nr_of_steps > get_test_utils("steps") else "PASS"

    folder_name = context.specification.file_name.split("\\")[-2]
    if folder_name != "tests":
        save_result_to_json(context.scenario.name, folder_name, context.specification.name, result)

    # assert not any(BaseTest.custom_asserts.failed_asserts)
    BaseTest.logger.log_info(f"The test \'{context.scenario.name}\' result is {result}")
    BaseTest.driver.close()
    BaseTest.driver.quit()
    BaseTest.driver = None
    BaseTest.finder = None
    BaseTest.custom_asserts = None
    BaseTest.logger = None


@after_spec
def after_spec(context: ExecutionContext):
    spec_file_path = context.specification.file_name
    spec_folder_name = spec_file_path.split("\\")[-2]
    spec_file_name = spec_file_path.split("\\")[-1].split(".")[0]
    if spec_folder_name != get_spec_property("spec_folder_name"):
        set_spec_property("spec_file_name", "")
        set_spec_property("spec_folder_name", spec_folder_name)
    set_spec_property("spec_file_name", get_spec_property("spec_file_name") + "," + spec_file_name if get_spec_property(
        "spec_file_name") else spec_file_name)


@after_step
def after_step():
    set_test_utils("steps", get_test_utils("steps") + 1)
