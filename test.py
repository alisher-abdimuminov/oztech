import requests

url = "https://oztech.uz/api/v1/users/signup/"

data = {
    "email": "alisher.abdimuminov.2005@gmail.com",
    "full_name": "Alisher",
    "password": "123",
}

res = requests.post(url=url, data=data)
print(res.text)
