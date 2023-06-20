import os.path
from datetime import datetime
from os import listdir
from os.path import isfile, join

from getgauge.python import Screenshots

from core.settings import BASE_PATH
from core.utils import replace_all_special_characters, get_the_latest_spec_folder
from core.json_methods import get_run_setting


class Logger:

    def __init__(self, test_name, spec_file_path):
        self.CRED = '\033[91m'
        self.CGREEN = '\33[32m'
        self.CWHITE = '\33[97m'
        self.CEND = '\033[0m'

        current_date = datetime.now().strftime("%d_%m_%Y")
        current_time = datetime.now().strftime("%H_%M_%S")
        current_timestamp = current_date + " " + current_time
        spec_file_name = spec_file_path.split("\\")[-1].split(".")[0]
        old_test_name = test_name
        test_name = replace_all_special_characters(test_name)

        if not os.path.isdir(BASE_PATH + f"\\run_results"):
            os.mkdir(BASE_PATH + f"\\run_results")
        if not os.path.isdir(BASE_PATH + f"\\run_results\\{current_date}"):
            os.mkdir(BASE_PATH + f"\\run_results\\{current_date}")

        self.log_file_path = BASE_PATH + f"\\run_results\\{current_date}\\{spec_file_name} {current_time}"
        spec_result_folder = get_the_latest_spec_folder(spec_file_name, BASE_PATH + f"\\run_results\\{current_date}")

        if get_run_setting("type") == "tags":
            spec_result_folder = get_the_latest_spec_folder(get_run_setting("tags").replace("|", "_"),
                                                            BASE_PATH + f"\\run_results\\{current_date}")
            tags_folder = get_run_setting("tags").replace("|", "_")
            self.log_file_path = BASE_PATH + f"\\run_results\\{current_date}\\{tags_folder} {current_time}"

        if not spec_result_folder:
            os.mkdir(self.log_file_path)

        else:
            path = BASE_PATH + f"\\run_results\\{current_date}\\{spec_result_folder}"
            spec_result_files = [f for f in listdir(path) if isfile(join(path, f))]
            flag = False

            for file in spec_result_files:
                if file == test_name:
                    flag = True
                    break

            if flag and not os.path.isdir(self.log_file_path):
                os.mkdir(self.log_file_path)

            if not flag:
                self.log_file_path = BASE_PATH + f"\\run_results\\{current_date}\\{spec_result_folder}"

        self.log_file_name = replace_all_special_characters(f"{test_name} ") + current_time + ".txt"
        print("\n" + self.CWHITE + current_timestamp + f"   TEST \'{old_test_name}\' STARTED" + self.CEND)

        with open(self.log_file_path + "\\" + self.log_file_name, 'w') as log_file:
            log_file.write(current_timestamp + f"   TEST \'{old_test_name}\' STARTED")

    def log_passed_assert(self, message):
        current_timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        output = "\n" + current_timestamp + "   PASSED: " + message
        print(self.CGREEN + output + self.CEND)
        with open(self.log_file_path + "\\" + self.log_file_name, 'a') as log_file:
            log_file.write(f"{output}")

    def log_failed_assert(self, message):
        current_timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        output = "\n" + current_timestamp + "   FAILED: " + message
        print(self.CRED + output + self.CEND)
        with open(self.log_file_path + "\\" + self.log_file_name, 'a') as log_file:
            log_file.write(f"{output}")
        Screenshots.capture_screenshot()

    def log_info(self, message):
        current_timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        output = "\n" + current_timestamp + "   INFO: " + message
        print(self.CWHITE + output + self.CEND)
        with open(self.log_file_path + "\\" + self.log_file_name, 'a') as log_file:
            log_file.write(f"{output}")
