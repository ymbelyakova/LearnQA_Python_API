from requests import Response
import json

class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_massage):
        try:
            response_as_dict = response.json()

        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"
        assert response_as_dict[name] == expected_value, error_massage

    @staticmethod
    def assert_json_has_keys(response: Response, keys:list):
        try:
            response_as_dict = response.json()

        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        for key in keys:
            assert key in response_as_dict, f"Response JSON doesn't have key '{key}'"

    @staticmethod
    def assert_json_has_no_key(response: Response, key):
        try:
            response_as_dict = response.json()

        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert key not in response_as_dict, f"Response JSON shouldn't have '{key}', but it's present."

    @staticmethod
    def assert_json_has_key(response: Response, key):
        try:
            response_as_dict = response.json()

        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert key in response_as_dict, f"Response JSON doesn't have key '{key}'"

    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, \
            f"Unexpected status code. Expected: {expected_status_code} Actual: {response.status_code}"