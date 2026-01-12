import requests
from lib.logger import Logger
import allure
from environment import ENV_OBJECT


class MyRequests():

    @staticmethod
    @allure.description("Sends POST request with set data, cookies and headers to given URL and returns corresponding response")
    def post (url:str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"POST request to URL {url}"):
            return MyRequests._send(url, data, headers, cookies, 'POST')

    @staticmethod
    @allure.description("Sends GET request with set data, cookies and headers to given URL and returns corresponding response")
    def get (url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"GET request to URL {url}"):
            return MyRequests._send(url, data, headers, cookies, 'GET')

    @staticmethod
    @allure.description("Sends PUT request with set data, cookies and headers to given URL and returns corresponding response")
    def put (url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"PUT request to URL {url}"):
            return MyRequests._send(url, data, headers, cookies, 'PUT')

    @staticmethod
    @allure.description("Sends POST request with set data, cookies and headers to given URL and returns corresponding response")
    def delete (url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"DELETE request to URL {url}"):
            return MyRequests._send(url, data, headers, cookies, 'DELETE')


    @staticmethod
    @allure.description("Allows to switch the Environment")
    def _send (url: str, data: dict, headers: dict, cookies: dict, method: str):

        url = f"{ENV_OBJECT.get_base_url()}{url}"
        #url = f"https://playground.learnqa.ru/api{url}"

        if headers is None:
            headers = {}

        if cookies is None:
            cookies = {}

        Logger.add_request(url, data, headers, cookies,method)

        if method == 'GET':
            response = requests.get(url, params = data, headers=headers, cookies=cookies)
        elif method == 'POST':
            response = requests.post(url, data = data, headers=headers, cookies=cookies)
        elif method == 'PUT':
            response = requests.put(url, data = data, headers=headers, cookies=cookies)
        elif method == 'DELETE':
            response = requests.delete(url, data = data, headers=headers, cookies=cookies)
        else:
            raise Exception(f"Bad HTTP Method: '{method}' was received")

        Logger.add_response(response)

        return response
