import requests
from lib.base_case import BaseCase

class TestHeaderPrint(BaseCase):
    expected_header = 'x-secret-homework-header'
    expected_header_value = 'Some secret value'

    def test_print_header(self):

        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        headers = response.headers
        assert headers, "No headers were returned by the response"
        '''
        for header in headers:
            print(header, headers[header])
        '''
        print(headers)
        return headers

    def test_print_header_value(self):
        received_headers = self.test_print_header()
        response2 = requests.get("https://playground.learnqa.ru/api/homework_header")
        received_value = self.get_header(response2, self.expected_header)
        assert received_value == self.expected_header_value, f"There is no expected header value {self.expected_header_value}"
        #print(f" The check is OK. There is a header named '{self.expected_header}' with value '{received_value}'")





