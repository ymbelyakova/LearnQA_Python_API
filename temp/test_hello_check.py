import pytest
import requests

class TestHelloCheck:
    names = [
        ("Yuliya"),
        ("Vitaliy"),
        ("")
    ]
    @pytest.mark.parametrize('name', names)
    def test_hello_check(self, name):
        url = "https://playground.learnqa.ru/api/hello"
        data = {'name': name}

        response = requests.get(url, params = data)
        assert response.status_code == 200, f"Wrong response code: {response.status_code}"

        response_dict = response.json()
        assert "answer" in response_dict, "There is no 'answer' field in response"



        if len(name) == 0:
            expected_answer = "Hello, someone"
        else:
            expected_answer = f"Hello, {name}"
        actual_answer = response_dict["answer"]
        assert actual_answer == expected_answer, f"Wrong answer: {actual_answer}"