import ctypes
import os
from datetime import datetime
from os import listdir
from os.path import isdir, join

import pythoncom
import win32com.client
import win32gui

from core.json_methods import get_run_setting, get_spec_property
from core.settings import BASE_PATH


def eliminate_all_special_characters(text):
    text = text.replace("[", "")
    text = text.replace("-", "")
    text = text.replace("+", "")
    text = text.replace(".", "")
    text = text.replace("^", "")
    text = text.replace(":", "")
    text = text.replace(",", "")
    text = text.replace("!", "")
    text = text.replace("@", "")
    text = text.replace("#", "")
    text = text.replace("$", "")
    text = text.replace("%", "")
    text = text.replace("&", "")
    text = text.replace("*", "")
    text = text.replace("(", "")
    text = text.replace(")", "")
    text = text.replace("<", "")
    text = text.replace(">", "")
    text = text.replace("?", "")
    text = text.replace("/", "")
    text = text.replace("\\", "")
    text = text.replace("\"", "")
    text = text.replace("\'", "")
    text = text.replace(";", "")
    text = text.replace("}", "")
    text = text.replace("{", "")
    text = text.replace("|", "")
    text = text.replace("]", "")

    return text


def make_a_schortcut(source_path, destination_path):
    pythoncom.CoInitialize()
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(destination_path)
    shortcut.Targetpath = source_path
    # shortcut.IconLocation = "path/to/icon"
    shortcut.WindowStyle = 7  # 7 - Minimized, 3 - Maximized, 1 - Normal
    shortcut.save()


def get_the_latest_spec_folder(spec_name, path):
    with disable_file_system_redirection():
        todays_folders = [f for f in listdir(path) if isdir(join(path, f))]
    my_folder = ""

    for folder in todays_folders:
        if folder[:-9] == spec_name and folder > my_folder:
            my_folder = folder

    return my_folder


class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection

    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))

    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)


def save_finished_tests_results():
    spec_folder_name = get_spec_property("spec_folder_name")
    spec_file_names = get_spec_property("spec_file_name").split(",")
    current_date = datetime.now().strftime("%d_%m_%Y")
    spec_result_folder_tags = None

    for spec_file_name in spec_file_names:
        spec_result_folder = get_the_latest_spec_folder(spec_file_name, BASE_PATH + f"\\run_results\\{current_date}")

        if get_run_setting("type") == "tags":
            spec_result_folder_tags = spec_result_folder = get_the_latest_spec_folder(
                get_run_setting("tags").replace("|", "_"), BASE_PATH + f"\\run_results\\{current_date}")

        report_path = BASE_PATH + f"\\reports\\html-report\\specs\\tests\\" \
                                  f"{spec_folder_name if spec_folder_name != 'tests' else ''}\\{spec_file_name}.html"
        result_path = BASE_PATH + f"\\run_results\\{current_date}\\{spec_result_folder}\\{spec_file_name}.html"

        with disable_file_system_redirection():
            with open(report_path, "r", encoding='utf8') as file:
                lines = file.readlines()
                new_lines = []
                new_base_path = BASE_PATH.replace('\\', '/')
                for line in lines:
                    if lines.index(line) != 19:
                        new_lines.append(line.replace("../../../../", f"{new_base_path}/reports/html-report/").
                                         replace("../../../", f"{new_base_path}/reports/html-report/").
                                         replace("../../", f"{new_base_path}/reports/html-report/"))
                    else:
                        new_lines.append(line.replace("src=\"../../../../", f"src=\"{new_base_path}/reports/html-report/").
                                         replace("src=\"../../../", f"src=\"{new_base_path}/reports/html-report/").
                                         replace("src=\"../../", f"src=\"{new_base_path}/reports/html-report/").
                                         replace("../", ""))

            with open(result_path, "w") as file:
                for line in new_lines:
                    file.write(line)

        os.startfile(result_path)

    report_path_index = BASE_PATH + f"\\reports\\html-report\\index.html"
    result_file_name = get_run_setting("tags").replace("|", "_")
    result_path_index = BASE_PATH + f"\\run_results\\{current_date}\\{spec_result_folder_tags}\\{result_file_name}.html"

    with disable_file_system_redirection():
        if get_run_setting("type") == "tags":
            with open(report_path_index, "r") as file:
                lines = file.readlines()
                new_lines_index = []
                new_base_path = BASE_PATH.replace('\\', '/')
                for line in lines:
                    new_lines_index.append(
                        line.replace("\"images", f"\"{new_base_path}/reports/html-report/images").replace("\"css", f"\"{new_base_path}/reports/html-report/css").replace(f"<a href=\"specs/tests/{spec_folder_name}/", f"<a href=\""))

            with open(result_path_index, "w") as file:
                for line in new_lines_index:
                    file.write(line)

            os.startfile(result_path_index)


def get_the_nr_of_steps_in_scenario(spec_path, scenario_name):
    with open(spec_path, "r") as file:
        lines = file.readlines()
    nr_of_steps = 0
    scenario_found = False

    for line in lines:
        if scenario_name in line:
            scenario_found = True

        elif scenario_found and '*' in line:
            nr_of_steps += 1

        elif '##' in line and scenario_found:
            break

    return nr_of_steps


def focus_on_driver_window():
    def windowEnumerationHandler(hwnd, top_windows):
        top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

    top_windows = []
    win32gui.EnumWindows(windowEnumerationHandler, top_windows)
    for i in top_windows:
        if i[1] == 'data:, - Google Chrome':
            win32gui.ShowWindow(i[0], 5)
            pythoncom.CoInitialize()
            shell = win32com.client.Dispatch("WScript.Shell")
            shell.SendKeys('%')
            win32gui.SetForegroundWindow(i[0])
            break
