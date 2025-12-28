import requests, json

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

real_methods = ["GET", "POST", "PUT", "DELETE"]
method_values = ["GET", "POST", "PUT", "DELETE"]
success = {"success":"!"} #Ожидаем получить, если тип запроса совпадает с переданным методом
error = "Wrong method provided" #Ожидаем получить, если тип запроса не совпадает с переданным методом

# 1. Делает http-запрос любого типа без параметра method, описать что будет выводиться в этом случае.
response1 = requests.get("https://playground.learnqa.ru/api/compare_query_type")
print(f"Текст ответа на запрос без параметра method = {response1.text} / Статус ответа на запрос без параметра method = {response1.status_code}\n")

# 2.  Делает http-запрос не из списка. Например, HEAD. Описать что будет выводиться в этом случае.
response2 = requests.head("https://playground.learnqa.ru/api/compare_query_type")
print(f"Текст ответа на запрос типа HEAD = {response2.text} / Статус ответа на запрос типа HEAD = {response2.status_code}\n")

def send_request(real_method, method_value):
    real = real_method.upper()
    mv = method_value.upper()

    if real == "GET":
        response = requests.get(url, params={"method": mv})
    elif real == "POST":
        response = requests.post(url, data={"method": mv})
    elif real == "PUT":
        response = requests.put(url, data={"method": mv})
    elif real == "DELETE":
        response = requests.delete(url, data={"method": mv})
    else:
        raise ValueError(f"Неподдерживаемый тип запроса {real}")

    try:
        # 3. Делает запрос с правильным значением method. Описать что будет выводиться в этом случае - в ответе получаем json {"success":"!"}
        j = response.json()
        #print(f"{real} / {mv} / {j}")
    except ValueError:
        j = {"error": response.text}
        #print(f"{real} / {mv} / {response.text}")
    return response.status_code, j

#  4. С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method. Например с GET-запросом передает значения параметра method равное ‘GET’, затем ‘POST’, ‘PUT’, ‘DELETE’ и так далее. И так для всех типов запроса. Найти такое сочетание, когда реальный тип запроса не совпадает со значением параметра, но сервер отвечает так, словно все ок. Или же наоборот, когда типы совпадают, но сервер считает, что это не так.
results = []

for real in real_methods:
    for mv in method_values:
        status, body = send_request(real, mv)
        results.append((real, mv, status, body))
        #print(f"{real} / method={mv} / status {status} / body {body}")


print("Найдены несоответствия (реальный тип запроса vs параметр method vs как api воспринял):")
for real, mv, status, body in results:
    try:
        if real == mv and (("success", "!") in body.items()):
            check = "OK"
            #print(f"{real} / method={mv}  status {status} / Получили {success} {check}")
        elif real == mv and (("error", "Wrong method provided") in body.items()):
            check = "NOK"
            print(f"Тип запроса {real} / method={mv}  status {status} / Ожидали получить {success}, а получили {error}")
        elif real != mv and (("error", "Wrong method provided") in body.items()):
            check = "OK"
            #print(f"{real} / method={mv}  status {status} / Получили {error} {check}")
        elif real != mv and (("success", "!") in body.items()):
            check = "NOK"
            print(f"Тип запроса {real} / method={mv}  status {status} / Ожидали получить {error}, а получили {body} {check}")
        else:
            print("Возможно изменился ответ от api/compare_query_type - нужно перепроверить")
    except json.JSONDecodeError:
        print("Неверный JSON: передан не поддерживаемый тип или метод запроса")