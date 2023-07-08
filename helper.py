import json
from httpx import get
from random import randint, choice

# class Wrapper:
#     def __init__(self, session):
#         self.session = session
#     def getProfile():
#         pass
#     def getProfile():
#         pass
#     def getProfile():
#         pass
#     def getProfile():
#         pass

class Utils:
    @staticmethod
    def getUsername():
        response = get(
            url = "https://randomuser.me/api/?nat=us&randomapi"
        )
        return response.json()["results"][0]["name"]["first"] + response.json()["results"][0]["name"]["last"] + str(randint(100000,900000))
    
    @staticmethod
    def getPassword():
        upperCase = "QWERTYUIOPASDFGHJKLZXCVBNM"
        lowerCase = "qwertyuiopasdfghjklzxcvbnm"
        digitsNum = "1234567890?!"
        return ''.join([choice(lowerCase + digitsNum + upperCase) for i in range(10)])
    
    @staticmethod
    def getBirthday():
        month = ["01","02","03","04","05","06","07","08","09","10","11","12"]
        return f"{randint(1990,2006)}-{choice(month)}-{randint(10,28)}"

# class Setup:
#     def __init__(self, session, token):
#         self.session = session
#         self.token = token
#         self.headers = {"authorization":self.token,"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

#     def getFlags(self):
#         checkList = [1000,2000,3000,4000,5000,6000,7000,8000,9000,1111,2222,3333,4444,5555,6666,7777,8888,9999,1122,2233,3344,4455,5566,6677,7788,8899,9900,1234,2345,3456,4567,5678,6789,7890]
#         response = self.session.get(
#             url = "https://discord.com/api/v9/users/@me",
#             headers = self.headers
#         )
#         print(response.text)
#         if response.status_code != 200:
#             status = "locked"
#         elif response.json()["flags"] == 0 or response.json()["public_flags"] == 0:
#             status = "unlocked"
#         elif response.json()["flags"] == 1048576 or response.json()["public_flags"] == 1048576:
#             status = "flagged"
#         elif response.json()["flags"] == 2199023255552 or response.json()["public_flags"] == 2199023255552:
#             status = "disabled"

#         if status in ["locked","disabled"]:
#             return status
#         else:
#             if response.json()["discriminator"] in checkList:
#                 return status + ":|"
#             else:
#                 return status
    
#     def getFriend(self):
#         self.headers["content-type"] = "application/json"
#         self.headers["x-context-properties"] = "eyJsb2NhdGlvbiI6IkFkZCBGcmllbmQifQ=="
#         response = self.session.post(
#             url = "https://discord.com/api/v9/users/@me/relationships",
#             headers = self.headers,
#             json = {
#                 "username": "louissiu",
#                 "discriminator": 1998
#             }
#         )
#         print(response.text)
#         if response.status_code == 204:
#             return True
#         else:
#             return False
