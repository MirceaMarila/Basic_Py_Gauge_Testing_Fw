from getgauge.python import step

from core.base_test import BaseTest as bt


@step("This is a step that logs HELLO WORLD!")
def log_hello_world():
    bt.logger.log_info("HELLO WORLD!")


@step("This is a step that logs the numbers between <start> and <end>")
def log_numbers_in_range(start, end):
    if not start.isnumeric():
        bt.logger.log_info(start + " is not a number!")

    elif not end.isnumeric():
        bt.logger.log_info(end + " is not a number!")

    else:
        for number in range(int(start), int(end)+1):
            bt.logger.log_info(str(number))


@step("The string <string1> is equal to the string <string2>")
def check_if_strings_are_equal(string1, string2):
    bt.custom_asserts.assert_equal(string1, string2, f"The string '{string1}' is equal to the string '{string2}'")


@step("This is a step that logs the elements of a table <table>")
def log_elements_of_table(table):
    table_dict = dict(zip(table.get_column_values_with_name("Key"), table.get_column_values_with_name("Value")))
    for key in table_dict.keys():
        bt.logger.log_info(f"'{key}' = '{table_dict[key]}'")
