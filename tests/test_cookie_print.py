import requests
from lib.base_case import BaseCase

class TestCookiePrint(BaseCase):
    expected_cookie = 'HomeWork'
    expected_cookie_value = 'hw_value'

    def test_print_coockie(self):

        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        cookies = response.cookies
        cookies_dict = cookies.get_dict()
        assert cookies, "No cookies were returned by the response"
        assert len(cookies_dict) ==1, "There are more cookies than expected"
        print(cookies_dict)
        return cookies_dict

    def test_cookie_check(self):
        received_cookies = self.test_print_coockie()
        response2 = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        for self.expected_cookie in received_cookies:
            received_value = self.get_cookie(response2, self.expected_cookie)
            assert received_value == self.expected_cookie_value, f"There is no expected cookie value {self.expected_cookie_value}"
            #print(f" The check is OK. There is a cookie named '{self.expected_cookie}' with value '{received_value}'")




