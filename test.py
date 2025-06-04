import requests

url = "https://oztech.uz/api/v1/users/verify/"

data = {
    "code": "7324",
    "email": "samdavfininst1@gmail.com",
    "full_name": "Alisher",
    "profession": "bekorchi",
    "password": "123",
}

res = requests.post(url=url, data=data)
print(res.text)
