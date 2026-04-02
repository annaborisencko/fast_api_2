import requests

data = requests.post(
    "http://localhost:80/api/v1/adv",
    json={
        "title": "Продается товар №1",
        "description": "Очень хороший товар? берите не пожалеете.",
        "price": 125.36,
        "user_id": 1
        }
)
print(data.status_code)
print(data.json())

# data = requests.get("http://127.0.0.1:8000/api/v1/todo/1")
# print(data.status_code)
# print(data.json())

# data = requests.patch("http://127.0.0.1:8000/api/v1/todo/1", json={"done": True, "title": "new_todo"})
# print(data.status_code)
# print(data.json())

# data = requests.get("http://127.0.0.1:8000/api/v1/todo/", params={"title": "new_todo", "important": True})
# print(data.status_code)
# print(data.json())

# data = requests.delete("http://127.0.0.1:8000/api/v1/todo/1")
# print(data.status_code)
# print(data.json())