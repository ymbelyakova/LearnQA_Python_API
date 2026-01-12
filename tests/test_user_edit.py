import pytest
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
import allure

@allure.epic("LearnQA user tests")
@allure.feature("Update user tests")
class TestUserEdit(BaseCase):
    def setup_method(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        self.email = register_data["email"]
        self.password = register_data["password"]
        # self.username = register_data["username"]
        # self.lastName = register_data["lastName"]
        self.firstName = register_data["firstName"]
        self.user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            "email": self.email,
            "password": self.password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        Assertions.assert_code_status(response1, 200)

        self.auth_sid = self.get_cookie(response2, "auth_sid")
        self.token = self.get_header(response2, "x-csrf-token")


    # Успешное изменение имени пользователя
    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.story("Successful change of user info for own user")
    @allure.description("Successful change of user info for own user: first name is changed")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_just_created_user_successfully(self):


        # EDIT
        new_name = "Changed Name"
        response3 = MyRequests.put(
            f"/user/{self.user_id}",
            headers = {"x-csrf-token": self.token},
            cookies = {"auth_sid": self.auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            f"Wrong name of the firstName after edit {self.firstName}"
        )

    # Неуспешная попытка изменить имя пользователя, будучи неавторизованным
    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.story("Fail to change user info without the authorization")
    @allure.description("Fail to change user first name without the authorization: no token and auth_sid were provided")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_edit_just_created_user_without_authorization_negative(self):


        # EDIT
        new_name = "Unauthorized Changed Name"
        response3 = MyRequests.put(
            f"/user/{self.user_id}",
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(
            response3,
            "error",
            "Auth token not supplied",
            f"Unexpected response message: {response3.content}"
        )

    # Неуспешная попытка изменить имя пользователя, будучи авторизованным другим пользователем
    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.story("Fail to change user info of not own user")
    @allure.description("Fail to change first name of not own user")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_edit_not_own_user_negative(self):


        # EDIT
        new_name = "Not Own Changed Name"

        response3 = MyRequests.put(
            f"/user/10",
            headers = {"x-csrf-token": self.token},
            cookies = {"auth_sid": self.auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(
            response3,
            "error",
            "This user can only edit their own data.",
            f"Unexpected response message {response3.content}"
        )

    # Неуспешная попытка изменить email пользователя на некорректный - без @
    @pytest.mark.regression
    @allure.story("Fail to change user email with incorrect one")
    @allure.description("Fail to change user email with incorrect one: @ is missing")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_user_email_with_no_at_negative(self):

        # EDIT
        new_email = "some_invalid_email.example.com"
        response3 = MyRequests.put(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
            data={"email": new_email}
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(
            response3,
            "error",
            "Invalid email format",
            f"Unexpected response message {response3.content}"
        )

    # Неуспешная попытка изменить firstName пользователя короткое <2символов
    @pytest.mark.regression
    @allure.story("Fail to change user info for too short")
    @allure.description("Fail to change user first name for too short <2 symbols")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_user_too_short_first_name_negative(self):
        # EDIT
        new_name = "F"
        response3 = MyRequests.put(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(
            response3,
            "error",
            "The value for field `firstName` is too short",
            f"Unexpected response message {response3.content}"
        )

