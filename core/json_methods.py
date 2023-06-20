import json

from core.settings import BASE_PATH


def get_run_setting(key):
    file = open(BASE_PATH + "\\core\\jsons\\run_settings.json")
    run_setting = json.load(file)
    file.close()
    return run_setting[key]


def set_run_setting(key, value):
    file = open(BASE_PATH + "\\core\\jsons\\run_settings.json")
    run_setting = json.load(file)
    run_setting[key] = value
    file.close()
    out_file = open(BASE_PATH + "\\core\\jsons\\run_settings.json", "w")
    json.dump(run_setting, out_file, indent=2)
    out_file.close()


def get_spec_property(key):
    file = open(BASE_PATH + "\\core\\jsons\\spec_properties.json")
    run_setting = json.load(file)
    file.close()
    return run_setting[key]


def set_spec_property(key, value):
    file = open(BASE_PATH + "\\core\\jsons\\spec_properties.json")
    run_setting = json.load(file)
    run_setting[key] = value
    file.close()
    out_file = open(BASE_PATH + "\\core\\jsons\\spec_properties.json", "w")
    json.dump(run_setting, out_file, indent=2)
    out_file.close()


def get_test_utils(key):
    file = open(BASE_PATH + "\\core\\jsons\\test_utils.json")
    run_setting = json.load(file)
    file.close()
    return run_setting[key]


def set_test_utils(key, value):
    file = open(BASE_PATH + "\\core\\jsons\\test_utils.json")
    run_setting = json.load(file)
    run_setting[key] = value
    file.close()
    out_file = open(BASE_PATH + "\\core\\jsons\\test_utils.json", "w")
    json.dump(run_setting, out_file, indent=2)
    out_file.close()


def save_result_to_json(scenario_name, folder_name, spec_name, result):
    file = open(BASE_PATH + "\\core\\jsons\\run_results.json")
    run_results = json.load(file)

    if folder_name not in run_results.keys():
        run_results[folder_name] = dict()
    if spec_name not in run_results[folder_name].keys():
        run_results[folder_name][spec_name] = dict()

    run_results[folder_name][spec_name][scenario_name] = result
    file.close()
    out_file = open(BASE_PATH + "\\core\\jsons\\run_results.json", "w")
    json.dump(run_results, out_file, indent=2)
    out_file.close()


def save_failed_test_results():
    with open(BASE_PATH + "\\.gauge\\failures.json") as failures_file:
        failures = json.load(failures_file)
        if failures['FailedItems']:
            for failed_spec in failures['FailedItems']:
                line = int(failed_spec.split(":")[-1].split("\"")[0])
                spec = failed_spec.split(":")[0].split("\"")[-1]
                with open(BASE_PATH + "\\" + spec) as spec_file:
                    lines = spec_file.readlines()
                    scenario = lines[line].split("## ")[-1]
                    with open(BASE_PATH + "\\core\\jsons\\run_results.json") as results_file:
                        results = json.load(results_file)
                        for specs in results.values():
                            for scenario_result_dict in specs.values():
                                for key in scenario_result_dict.keys():
                                    if key == scenario:
                                        specs.values()[key] = "FAIL"


def save_failed_items():
    failures_file = open(BASE_PATH + "\\.gauge\\failures.json")
    failed_items_file = open(BASE_PATH + "\\core\\jsons\\failed_items.json")

    failures = json.load(failures_file)
    failed_items = json.load(failed_items_file)

    if failures['FailedItems']:
        for failed_spec in failures['FailedItems']:
            if failed_spec not in failed_items['FailedItems']:
                failed_items['FailedItems'].append(failed_spec)

    failures_file.close()
    failed_items_file.close()

    failed_items_file = open(BASE_PATH + "\\core\\jsons\\failed_items.json", "w")
    json.dump(failed_items, failed_items_file, indent=2)
    failed_items_file.close()


def get_failed_items():
    failed_items_file = open(BASE_PATH + "\\core\\jsons\\failed_items.json")
    failed_items = json.load(failed_items_file)['FailedItems']
    failed_items_file.close()

    return failed_items


def delete_failed_items(item):
    failed_items_file = open(BASE_PATH + "\\core\\jsons\\failed_items.json")
    failed_items = json.load(failed_items_file)
    failed_items_file.close()

    failed_items_file = open(BASE_PATH + "\\core\\jsons\\failed_items.json", "w")
    failed_items['FailedItems'].remove(item)
    json.dump(failed_items, failed_items_file, indent=2)
    failed_items_file.close()
