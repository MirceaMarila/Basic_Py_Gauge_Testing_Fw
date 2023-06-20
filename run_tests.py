from core.settings import BASE_PATH
from core.utils import save_finished_tests_results
from core.json_methods import set_run_setting, set_spec_property, get_test_utils, save_failed_test_results, \
    save_failed_items, get_failed_items, delete_failed_items
import os
import psutil
from os import listdir
from os.path import isdir, join


os.chdir(BASE_PATH)
run_type = input("What do you want to run? spec/tags/folder/failed/all\n")
set_spec_property("spec_file_name", "")
set_spec_property("spec_folder_name", "")
command = None
commands = []

if run_type.lower() == "spec":
    set_run_setting("type", "spec")
    set_run_setting("tags", "")
    folder_name = input("In which folder there is this spec ?\n")
    spec_name = input("What spec do you want to run ?\n")
    command = f"gauge run specs/tests/{folder_name}/{spec_name}.spec"

elif run_type.lower() == "tags":
    set_run_setting("type", "tags")
    tags = input("What tags do you want to run ? tag1/tag1|tag2\n")
    set_run_setting("tags", tags)
    command = f"gauge run --tags=\"{tags}\" specs"

elif run_type.lower() == "all":
    set_run_setting("type", "spec")
    set_run_setting("tags", "")

    mypath = BASE_PATH + "\\specs\\tests"
    subfolders = [f for f in listdir(mypath) if isdir(join(mypath, f))]
    command = None
    for folder in subfolders:
        commands.append(f"gauge run specs/tests/{folder}")

elif run_type.lower() == "folder":
    set_run_setting("type", "spec")
    set_run_setting("tags", "")
    folder_name = input("What folder do you want to run ?\n")
    command = f"gauge run specs/tests/{folder_name}"

elif run_type.lower() == "failed":
    set_run_setting("type", "spec")
    set_run_setting("tags", "")
    command = None

    failed_items = get_failed_items()
    for item in failed_items:
        commands.append(f"gauge run {item}")
        delete_failed_items(item)

elif 'test' in run_type.lower():
    set_run_setting("type", "spec")
    set_run_setting("tags", "")
    command = f"gauge run specs/tests/{run_type}.spec"

else:
    print("ERROR: UNKNOWN RUN TYPE")

if command:
    os.system(command)
    save_finished_tests_results()

elif commands:
    for command in commands:
        os.system(command)
        save_finished_tests_results()
        save_failed_items()

save_failed_test_results()


try:
    p = psutil.Process(get_test_utils("driver_pid"))
    p.kill()  # or p.terminate()

except:
    pass
