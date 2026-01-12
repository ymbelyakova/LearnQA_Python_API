from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure
import pytest

@allure.epic("LearnQA user tests")
@allure.feature("Get user info tests")
class TestUserGet(BaseCase):

    # При неавторизованном запросе о пользователе получаем только его username
    @pytest.mark.regression
    @allure.story("Provide just username in case of unauthorized request")
    @allure.description("Returns just username in case of unauthorized request")
    @allure.severity(allure.severity_level.NORMAL)
    #@allure.title("Get username in case of unauthorized request")
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_no_key(response, "email")
        Assertions.assert_json_has_no_key(response, "password")
        Assertions.assert_json_has_no_key(response, "firstName")
        Assertions.assert_json_has_no_key(response, "lastName")

    # При авторизованном запросе о своем пользователе получаем всю ожидаемую информацию
    @pytest.mark.regression
    @allure.story("Provide all info about own user in case of successful login")
    @allure.description("Return all info about own user in case of successful login")
    @allure.severity(allure.severity_level.CRITICAL)
    #@allure.title("Return info about own user in case of successful login")
    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        expected_fields = ["username", "email", "firstName", "lastName"]

        response1 = MyRequests.post("/user/login", data=data)
        Assertions.assert_code_status(response1, 200)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(
            f"/user/{user_id_from_auth_method}",
            headers = {"x-csrf-token" : token},
            cookies = {"auth_sid" : auth_sid}
        )

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_keys(response2, expected_fields)
        Assertions.assert_json_has_no_key(response2, "password")

    # При авторизованном запросе о другом пользователе получаем только его username
    @pytest.mark.regression
    @allure.story("Provide just username of not own user in case of successful login")
    @allure.description("Returns just username of not own user own user in case of successful login")
    @allure.severity(allure.severity_level.NORMAL)
    #@allure.title("Returns just username of not own user in case of successful login")
    def test_get_user_details_auth_as_another_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)
        Assertions.assert_code_status(response1, 200)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")
        assert user_id_from_auth_method != 3, f"Unexpected user_id from auth_method {user_id_from_auth_method}"

        response2 = MyRequests.get(
            f"/user/3",
            headers = {"x-csrf-token" : token},
            cookies = {"auth_sid" : auth_sid}
        )

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_no_key(response2, "email")
        Assertions.assert_json_has_no_key(response2, "password")
        Assertions.assert_json_has_no_key(response2, "firstName")
        Assertions.assert_json_has_no_key(response2, "lastName")

