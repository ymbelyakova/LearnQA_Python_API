from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests

class TestUserDelete(BaseCase):

    # Успешное удаление нового созданного пользователя
    def test_user_delete_successfully(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            "email": email,
            "password": password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE
        response3 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
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
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response4, 404)
        assert response4.content.decode("utf-8") == "User not found", f"Unexpected error message {response4.content}"




    # Невозможно удалить пользователя с id<=5
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
        response3 = MyRequests.get(
            "/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_has_keys(response3, ["id", "username", "email", "firstName", "lastName"])

        # Невозможно удалить пользователя будучи авторизованным другим пользователем

    def test_user_delete_not_own_user_negative(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            "email": 'vinkotov@example.com',
            "password": '1234'
        }

        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE
        response3 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(
            response3,
            "error",
            "Please, do not delete test users with ID 1, 2, 3, 4 or 5.",
            f"Unexpected error message {response3.content}"
        )

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response4, 200)
        Assertions.assert_json_has_key(response4, "username")

