import json
from httpx import get
from random import randint, choice
from hashlib import md5
from fake_useragent import UserAgent
import string
import time

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
informations = {
    "hswScript": "44fa09c"
}
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
    
    @staticmethod
    def getUseragent():
        resp = get("https://www.whatismybrowser.com/guides/the-latest-user-agent/chrome").text
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + resp.split("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/")[1].split(".0.0.0 Safari/537.36")[0] + ".0.0.0 Safari/537.36"

    @staticmethod
    def getCaptchaV():
        resp = get("https://hcaptcha.com/1/api.js").text
        s = resp.find("https://newassets.hcaptcha.com/captcha/") + 42
        f = resp[s:].find("/") + s
        return resp[s:f]

    @staticmethod
    def getCaptchaH():
        response = get(
            url = f"https://newassets.hcaptcha.com/c/{informations['hswScript']}/hsw.js"
        )
        return response.text

    @staticmethod
    def getHeaders(userAgent):
        base = {   
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en;q=0.9",
            "Dnt": "1",
            "Sec-Ch-Ua": "\"Not.A\/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "Windows",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": userAgent
        }
        return base
        
#  I didn't made this part, this is from xtekky's github G4F, gpt4free, thanks for the contribution ...
class Solver:
    @classmethod
    def md5(self, text):
        return md5(text.encode()).hexdigest()[::-1]

    @classmethod
    def get_api_key(self, user_agent):
        part1 = str(randint(0, 10**11))
        part2 = self.md5(user_agent+self.md5(user_agent+self.md5(user_agent+part1+"x")))
        return f"tryit-{part1}-{part2}"

    @classmethod
    def create(self, session, messages):
        user_agent = UserAgent().random
        api_key = self.get_api_key(user_agent)
        headers = {
          "api-key": api_key,
          "user-agent": user_agent
        }
        files = {
          "chat_style": (None, "chat"),
          "chatHistory": (None, json.dumps(messages))
        }

        response = session.post("https://api.deepai.org/chat_response", headers=headers, files=files, stream=True)

        for chunk in response.iter_content(chunk_size=None):
            response.raise_for_status()
            yield chunk.decode()

class Completion:
    @classmethod
    def create(self, prompt, session):
        return Solver.create(session,[{"role": "user", "content": prompt}])
