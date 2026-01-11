from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from random import choices
import string
import pytest


class TestUserRegister(BaseCase):
    required_params = [
        ("email"),
        ("password"),
        ("username"),
        ("firstName"),
        ("lastName")
    ]


    # Успешная регистрация пользователя
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")


    # Пользователь не зарегистрирован, т. к. email уже существует
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data = data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content: {response.content}"

    # Пользователь не зарегистрирован, т. к. email невалиден - нет @
    def test_create_user_with_invalid_email(self):
        email = 'learnqa_no_at_example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", f"Unexpected response content: {response.content}"

    # Пользователь не зарегистрирован, т. к. длина имени <2 символов
    def test_create_user_with_invalid_short_name(self):
        data = self.prepare_registration_data()
        name = ''.join(choices(string.ascii_letters, k=1))
        data['firstName'] = name
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too short", f"Unexpected response content: {response.content}"

    # Пользователь не зарегистрирован, т. к. длина имени >250 символов
    def test_create_user_with_invalid_long_name(self):
        data = self.prepare_registration_data()
        name = ''.join(choices(string.ascii_letters, k=251))
        data['firstName'] = name
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too long", f"Unexpected response content: {response.content}"

    # Пользователь не зарегистрирован, т. к. не передан один из необходимых параметров
    @pytest.mark.parametrize('condition', required_params)
    def test_negative_create_user(self, condition):
        data = self.prepare_registration_data()

        if condition == "email":
            data.pop("email")
            response2 = MyRequests.post("/user/", data = data)
            Assertions.assert_code_status(response2, 400)
            assert response2.content.decode("utf-8") == f"The following required params are missed: {condition}"
        elif condition == "password":
            data.pop("password")
            response2 = MyRequests.post("/user/", data=data)
            Assertions.assert_code_status(response2, 400)
            assert response2.content.decode("utf-8") == f"The following required params are missed: {condition}"
        elif condition == "username":
            data.pop("username")
            response2 = MyRequests.post("/user/", data=data)
            Assertions.assert_code_status(response2, 400)
            assert response2.content.decode("utf-8") == f"The following required params are missed: {condition}"
        elif condition == "firstName":
            data.pop("firstName")
            response2 = MyRequests.post("/user/", data=data)
            Assertions.assert_code_status(response2, 400)
            assert response2.content.decode("utf-8") == f"The following required params are missed: {condition}"
        elif condition == "lastName":
            data.pop("lastName")
            response2 = MyRequests.post("/user/", data=data)
            Assertions.assert_code_status(response2, 400)
            assert response2.content.decode("utf-8") == f"The following required params are missed: {condition}"
        else:
            print("Unknown condition is set")
