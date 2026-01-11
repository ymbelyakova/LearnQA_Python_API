import requests
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests

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

        self.auth_sid = self.get_cookie(response2, "auth_sid")
        self.token = self.get_header(response2, "x-csrf-token")


    # Успешное изменение имени пользователя
    def test_edit_just_created_user(self):


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
    def test_edit_just_created_user_without_authorization(self):


        # EDIT
        new_name = "Changed Name"
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
    def test_edit_not_own_user(self):


        # EDIT
        new_name = "Changed Name"
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

