import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
redirect_count = len(response.history)
print(f"Количество редиректов = {redirect_count}")
print(f"Итоговый URL {response.url}")
#print(response.status_code)
'''
for r in response.history:
    print(f"Код ответа {r.status_code}, URL запроса {r.url}, URL редиректа {r.headers['Location']}")
'''
