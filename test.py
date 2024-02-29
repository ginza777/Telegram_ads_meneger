import requests
import uuid
# Ma'lumotlar
url = "https://login.emaktab.uz/login"
id=str(uuid.uuid4())
data = {
    "exceededAttempts": "False",
    "ReturnUrl": "",
    "FingerprintId": "",
    "login": "Asrayevarano",
    "password": "Kod123",
    "Captcha.Input": "",
    "Captcha.Id":id
}

# So'rovni jo'natish
response = requests.post(url, data=data)

# Natijani tekshirish
if response.status_code == 200:
    print(response.text)
    print(id)
    print("So'rov muvaffaqiyatli jo'natildi.")
else:
    print("Xatolik yuz berdi:", response.status_code)
