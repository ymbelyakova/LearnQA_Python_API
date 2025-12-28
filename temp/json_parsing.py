import json

'''Предложение по улучшению. 
Для примера из https://gist.github.com/KotovVitaliy/83e4eeabdd556431374dfc70d0ba9d37 
Заменить второе сообщение на более правильное: And this is the second message'''
json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is the second message","timestamp":"2021-06-04 16:41:01"}]}'
try:
    data = json.loads(json_text)
    msgs = data.get("messages", [])
    if len(msgs) > 1:
        print(msgs[1].get('message'))
    else:
        print("Второго сообщения нет")
except json.JSONDecodeError:
    print("Неверный JSON")


