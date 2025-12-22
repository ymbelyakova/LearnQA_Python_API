import requests, time
from json import JSONDecodeError

response1 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
try:
    data1 = response1.json()
    given_token = data1["token"]
    expected_time = data1["seconds"]
    #print(f"Получили токен {given_token}, время до завершения {expected_time}")
    #Отправляем запрос с токеном до завершения задачи
    response2 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params = {"token": given_token})
    data2 = response2.json()
    if data2["status"] == "Job is NOT ready":
        check = "OK"
        print(f"Задача не завершена, получили в ответ status = {data2['status']} - {check}")
    else:
        check = "NOK"
        print(f"Задача не завершена, получили в ответ status = {data2['status']} - {check}")
    print(f"До завершения задачи нужно подождать {expected_time} секунд...")
    #Отправляем запрос с токеном после ожидаемого завершения задачи
    time.sleep(expected_time)
    response3 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": given_token})
    data3 = response3.json()
    if data3["status"] == "Job is ready" and ("result", "42") in data3.items():
        check = "OK"
        print(f"Задача завершена, получили в ответ status = {data3['status']}, result = {data3['result']} - {check}")
    else:
        check = "NOK"
        print(f"Ошибка, ожидали получить status = Job is ready и result = 42, получили в ответ {data3} - {check}")
except JSONDecodeError:
    print("Вернулся неверный JSON")




