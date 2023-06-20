class CustomAsserts:
    
    def __init__(self, logger):
        self.failed_asserts = []
        self.logger = logger

    def assert_true(self, boolean, message, element=None):
        if element:
            element.highlight(effect_time=0.1, color="blue")

        if boolean:
            if element:
                element.highlight(effect_time=0.1, color="green")
            self.logger.log_passed_assert(message)
            self.failed_asserts.append(False)

        else:
            if element:
                element.highlight(color="red")
            self.logger.log_failed_assert(message)
            self.failed_asserts.append(True)

        assert boolean is True, message

    def assert_false(self, boolean, message, element=None):
        if element:
            element.highlight(effect_time=0.1, color="blue")

        if not boolean:
            if element:
                element.highlight(effect_time=0.1, color="green")
            self.logger.log_passed_assert(message)
            self.failed_asserts.append(False)

        else:
            if element:
                element.highlight(color="red")
            self.logger.log_failed_assert(message)
            self.failed_asserts.append(True)

        assert boolean is False, message

    def assert_equal(self, expected, found, message, element=None):
        if element:
            element.highlight(effect_time=0.1, color="blue")

        if expected == found:
            if element:
                element.highlight(effect_time=0.1, color="green")
            self.logger.log_passed_assert(message)
            self.failed_asserts.append(False)

        else:
            if element:
                element.highlight(color="red")
            self.logger.log_failed_assert(message)
            self.failed_asserts.append(True)

        assert expected == found, message
    
    def assert_not_equal(self, expected, found, message, element=None):
        if element:
            element.highlight(effect_time=0.1, color="blue")

        if expected != found:
            if element:
                element.highlight(effect_time=0.1, color="green")
            self.logger.log_passed_assert(message)
            self.failed_asserts.append(False)

        else:
            if element:
                element.highlight(color="red")
            self.logger.log_failed_assert(message)
            self.failed_asserts.append(True)

        assert expected != found, message
