import requests
import json
from pprint import pprint

print("##### Создаем пользователя №1 с правами пользователя #####")
data = requests.post(
    "http://localhost:80/api/v1/user",
    json={
        "name": "user_1",
        "password": "password_1"
        }
)
print(data.status_code)
print(data.json(), "\n")


print("##### Создаем пользователя №2 с правами админа #####")
data = requests.post(
    "http://localhost:80/api/v1/user",
    json={
        "name": "user_2",
        "password": "password_2",
        "role": "admin"
        }
)
print(data.status_code)
print(data.json(), "\n")


print("##### Создаем пользователя №3 с правами пользователя #####")
data = requests.post(
    "http://localhost:80/api/v1/user",
    json={
        "name": "user_3",
        "password": "password_3"
        }
)
print(data.status_code)
print(data.json(), "\n")


print("##### Получаем пользователя с id=1 #####")
data = requests.get("http://localhost:80/api/v1/user/1")
print(data.status_code)
print(data.json(), "\n")


print("##### Меняем пользователя с id=1 без авторизации #####")
data = requests.patch(
    "http://localhost:80/api/v1/user/1",
    json={
        "role": "admin"
    }
    )
print(data.status_code)
print(data.json(), "\n")


print("##### Удаляем пользователя с id=1 без авторизации #####")
data = requests.delete("http://localhost:80/api/v1/user/1")
print(data.status_code)
print(data.json(), "\n")


print("##### Авторизуемся под пользователем №1 с правами пользователя #####")
data = requests.post(
    "http://localhost:80/api/v1/login",
    json={
        "name": "user_1",
        "password": "password_1"
        }
)
print(data.status_code)
print(data.json(), "\n")

token = data.json()["token"]


print("##### Меняем свои учетные данные #####")
data = requests.patch(
    "http://localhost:80/api/v1/user/1",
    json={
        "name": "user_1_1"
    },
    headers={"Authorization": f"Bearer {token}"}
    )
print(data.status_code)
print(data.json(), "\n")


print("##### Меняем чужие учетные данные #####")
data = requests.patch(
    "http://localhost:80/api/v1/user/2",
    json={
        "name": "user_2_1"
    },
    headers={"Authorization": f"Bearer {token}"}
    )
print(data.status_code)
print(data.json(), "\n")


print("##### Создаем объявление №1 #####")
data = requests.post(
    "http://localhost:80/api/v1/advertisement",
    json={
        "title": "Продается товар №1",
        "description": "Очень хороший товар? берите не пожалеете.",
        "price": 1100.00
        },
    headers={"Authorization": f"Bearer {token}"}
)
print(data.status_code)
print(data.json(), "\n")

print("##### Создаем объявление №2 #####")
data = requests.post(
    "http://localhost:80/api/v1/advertisement",
    json={
        "title": "Продается товар №2",
        "description": "Очень хороший товар, берите не пожалеете.",
        "price": 1200.00
        },
    headers={"Authorization": f"Bearer {token}"}
)
print(data.status_code)
print(data.json(), "\n")

print("##### Создаем объявление №3 #####")
data = requests.post(
    "http://localhost:80/api/v1/advertisement",
    json={
        "title": "Продается товар №3",
        "description": "Очень хороший товар, берите не пожалеете.",
        "price": 1100.00
        },
    headers={"Authorization": f"Bearer {token}"}
)
print(data.status_code)
print(data.json(), "\n")


print("##### Получаем объявление с id=1 #####")
data = requests.get("http://localhost:80/api/v1/advertisement/1")
print(data.status_code)
print(data.json(), "\n")


print("##### Изменяем объявление с id=1 под учетной записью владельца#####")
data = requests.patch(
    "http://localhost:80/api/v1/advertisement/1",
    json={
        "description": "Очень хороший товар, лучше не найдете.", 
        "price": 1500.00
        },
    headers={"Authorization": f"Bearer {token}"}
)
print(data.status_code)
print(data.json(), "\n")
data = requests.get("http://localhost:80/api/v1/advertisement/1")
print(data.json(), "\n")


print("##### Ищем объявления с наименованием, содержащим текст 'товар №1' #####")
data = requests.get("http://localhost:80/api/v1/advertisement", params={"title": "товар №1"})
print(data.status_code)
pprint(data.json())
print("\n")

print("##### Ищем объявления c описанием, содержащим текст 'хороший' #####")
data = requests.get("http://localhost:80/api/v1/advertisement", params={"description": "хороший", "limit": 2, "offset": 1})
print(data.status_code)
pprint(data.json())
print("\n")

print("##### Ищем объявления с ценой в интервале от 1200 до 1500 включительно #####")
data = requests.get("http://localhost:80/api/v1/advertisement", params={"price_min": 1200, "price_max": 1500})
print(data.status_code)
pprint(data.json())
print("\n")

print("##### Ищем объявления с ценой от 1200 включительно #####")
data = requests.get("http://localhost:80/api/v1/advertisement", params={"price_min": 1200})
print(data.status_code)
pprint(data.json())
print("\n")

print("##### Ищем объявления с ценой до 1200 включительно #####")
data = requests.get("http://localhost:80/api/v1/advertisement", params={"price_max": 1200})
print(data.status_code)
pprint(data.json())
print("\n")


print("##### Создаем объявление с ценой <= 0 #####")
data = requests.post(
    "http://localhost:80/api/v1/advertisement",
    json={
        "title": "Продается товар №5",
        "description": "Очень хороший товар? берите не пожалеете.",
        "price": 0.00
        },
    headers={"Authorization": f"Bearer {token}"}
)
print(data.status_code)
print(data.json(), "\n")


print("##### Изменяем объявление с id=2, пробуем передать цену <= 0 #####")
data = requests.patch(
    "http://localhost:80/api/v1/advertisement/2",
    json={
        "description": "Очень хороший товар, лучше не найдете.", 
        "price": -300.00
        },
    headers={"Authorization": f"Bearer {token}"}
)
print(data.status_code)
print(data.json(), "\n")


print("##### Авторизуемся под пользователем №3 с правами пользователя #####")
data = requests.post(
    "http://localhost:80/api/v1/login",
    json={
        "name": "user_3",
        "password": "password_3"
        }
)
print(data.status_code)
print(data.json(), "\n")

token = data.json()["token"]


print("##### Изменяем чужое объявление с id=2 с правами пользователя #####")
data = requests.patch(
    "http://localhost:80/api/v1/advertisement/2",
    json={
        "description": "Очень хороший товар, лучше не найдете.", 
        "price": 3300.00
        },
    headers={"Authorization": f"Bearer {token}"}
)
print(data.status_code)
print(data.json(), "\n")


print("##### Удаляем чужое объявление с id=1 с правами пользователя #####")
data = requests.delete(
    "http://localhost:80/api/v1/advertisement/1",
    headers={"Authorization": f"Bearer {token}"}
)
print(data.status_code)
print(data.json(), "\n")

print("##### Авторизуемся под пользователем №2 с правами адмиинистратора #####")
data = requests.post(
    "http://localhost:80/api/v1/login",
    json={
        "name": "user_2",
        "password": "password_2"
        }
)
print(data.status_code)
print(data.json(), "\n")

token = data.json()["token"]

print("##### Меняем чужие учетные данные под админом #####")
data = requests.patch(
    "http://localhost:80/api/v1/user/1",
    json={
        "name": "user_1_1"
    },
    headers={"Authorization": f"Bearer {token}"}
    )
print(data.status_code)
print(data.json(), "\n")


print("##### Изменяем чужое объявление с id=1 под учетной записью администратора #####")
data = requests.patch(
    "http://localhost:80/api/v1/advertisement/1",
    json={
        "description": "Очень хороший товар, лучше не найдете.", 
        "price": 2500.00
        },
    headers={"Authorization": f"Bearer {token}"}
)
print(data.status_code)
print(data.json(), "\n")
data = requests.get("http://localhost:80/api/v1/advertisement/1")
print(data.json(), "\n")


print("##### Удаляем чужое объявление с id=1 с правами администратора #####")
data = requests.delete(
    "http://localhost:80/api/v1/advertisement/1",
    headers={"Authorization": f"Bearer {token}"}
)
print(data.status_code, "\n")


print("##### Удаляем другого пользователя с правами администратора #####")
data = requests.delete(
    "http://localhost:80/api/v1/user/1",
    headers={"Authorization": f"Bearer {token}"}
)
print(data.status_code, "\n")


