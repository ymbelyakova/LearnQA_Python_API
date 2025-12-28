import requests
payload = {"login": "secret_login", "password": "secret_pass"}
response1 = requests.post("https://playground.learnqa.ru/ajax/api/get_auth_cookie", data = payload)
cookie_value = response1.cookies.get('auth_cookie')

cookies = {}
if cookie_value is not None:
    cookies.update({"auth_cookie": cookie_value})

response2 = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies = cookies)
print(response2.text)


'''
from json import JSONDecodeError
import requests

response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", params = {"method": "GET"})
print(response.text)
print(response.headers)

'''

'''
payload = {"name": "Yuliya"}
"""response = requests.get("https://playground.learnqa.ru/api/get_text", params = payload)"""
response = requests.get("https://playground.learnqa.ru/api/hello", params = payload)
print(response.text)
try:
    parsed_json_text = response.json()
    print(parsed_json_text["answer"])
except JSONDecodeError:
    print("Response is not a JSON format")
'''

'''
response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
redirect_count = len(response.history)
print(f"Количество редиректов = {redirect_count}")
print(f"Итоговый URL {response.url}")
#print(response.status_code)

for r in response.history:
    print(f"Код ответа {r.status_code}, URL запроса {r.url}, URL редиректа {r.headers['Location']}")
'''

'''
header = {"some_header": "The best day is today."}
response = requests.get("https://playground.learnqa.ru/api/show_all_headers", headers=header)
print(f"Заголовки запроса {response.text}")
print(f"Заголовки ответа {response.headers}")

'''

