from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime
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

    # Генерация email
    def setup_method(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{base_part}{random_part}@{domain}"

    # Успешная регистрация пользователя
    def test_create_user_successfully(self):
        data = {
            'email': self.email,
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa'
        }
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")




    # Пользователь не зарегистрирован, т. к. email уже существует
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = {
            'email': email,
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa'
        }

        response = MyRequests.post("/user/", data = data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content: {response.content}"

    # Пользователь не зарегистрирован, т. к. email невалиден - нет @
    def test_create_user_with_invalid_email(self):
        data = {
            'email': 'learnqa_no_at_example.com',
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa'
        }
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", f"Unexpected response content: {response.content}"

    # Пользователь не зарегистрирован, т. к. длина имени <2 символов
    def test_create_user_with_invalid_short_username(self):
        name = ''.join(choices(string.ascii_letters, k=1))
        data = {
            'email': self.email,
            'password': '123',
            'username': name,
            'firstName': 'learnqa',
            'lastName': 'learnqa'
        }
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too short", f"Unexpected response content: {response.content}"

    # Пользователь не зарегистрирован, т. к. длина имени >250 символов
    def test_create_user_with_invalid_long_username(self):
        name = ''.join(choices(string.ascii_letters, k=251))
        data = {
            'email': self.email,
            'password': '123',
            'username': name,
            'firstName': 'learnqa',
            'lastName': 'learnqa'
        }
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too long", f"Unexpected response content: {response.content}"

    # Пользователь не зарегистрирован, т. к. не передан один из необходимых параметров
    @pytest.mark.parametrize('condition', required_params)
    def test_negative_create_user(self, condition):
        data = {
            'email': self.email,
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa'
        }
        #new_data = data.copy()
        if condition == "email":
            data.pop("email")
            response2 = MyRequests.post("/user/", data = data)
            assert response2.content.decode("utf-8") == f"The following required params are missed: {condition}"
        elif condition == "password":
            data.pop("password")
            response2 = MyRequests.post("/user/", data=data)
            assert response2.content.decode("utf-8") == f"The following required params are missed: {condition}"
        elif condition == "username":
            data.pop("username")
            response2 = MyRequests.post("/user/", data=data)
            assert response2.content.decode("utf-8") == f"The following required params are missed: {condition}"
        elif condition == "firstName":
            data.pop("firstName")
            response2 = MyRequests.post("/user/", data=data)
            assert response2.content.decode("utf-8") == f"The following required params are missed: {condition}"
        elif condition == "lastName":
            data.pop("lastName")
            response2 = MyRequests.post("/user/", data=data)
            assert response2.content.decode("utf-8") == f"The following required params are missed: {condition}"
        else:
            print("Unknown condition is set")
