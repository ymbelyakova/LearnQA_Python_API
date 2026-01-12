from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
import allure
import pytest

@allure.epic("LearnQA user tests")
@allure.feature("Delete user tests")
class TestUserDelete(BaseCase):

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


    # Успешное удаление нового созданного пользователя
    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.story("Successful delete of own user")
    @allure.description("Successful delete of own user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_user_delete_successfully(self):

        # DELETE
        response3 = MyRequests.delete(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_value_by_name(
            response3,
            "success",
            "!",
            f"Unexpected message {response3.content}"
        )

        # GET
        response4 = MyRequests.get(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )


        Assertions.assert_code_status(response4, 404)
        assert response4.content.decode("utf-8") == "User not found", f"Unexpected error message {response4.content}"




    # Невозможно удалить пользователя с id<=5
    @pytest.mark.regression
    @allure.story("Fail to delete reserved own user")
    @allure.description("Fail to delete reserved own user with id <=5")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_user_delete_undeletable_user_negative(self):
        # LOGIN
        login_data = {
            "email":  'vinkotov@example.com',
            "password": '1234'
        }

        response1 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # DELETE
        response2 = MyRequests.delete(
            "/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response2, 400)
        Assertions.assert_json_value_by_name(
            response2,
            "error",
            "Please, do not delete test users with ID 1, 2, 3, 4 or 5.",
            f"Unexpected error message {response2.content}"
        )

        # GET
        expected_fields = ["id", "username", "email", "firstName", "lastName"]
        response3 = MyRequests.get(
            "/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_has_keys(response3, expected_fields)

    # Невозможно удалить пользователя будучи авторизованным другим пользователем
    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.story("Fail to delete not own user")
    @allure.description("Fail to delete not own user")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_user_delete_not_own_user_negative(self):

        # DELETE

        response3 = MyRequests.delete(
            f"/user/10",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(
            response3,
            "error",
            "This user can only delete their own account.",
            f"Unexpected error message {response3.content}"
        )

