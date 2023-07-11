from hcaptcha.collectHsw import FunctionHsw
from hcaptcha.motionData import MotionData
from urllib.parse import urlencode
from helper import Utils, Solver
from random import randint, choice
from json import dumps, loads
from time import time
import json
import os

class Captcha:
    def __init__(self, session, userAgent):
        self.session = session
        self.userAgent = userAgent
        self.version = Utils.getCaptchaV()
        self.solvedAnswers = []
        self.textLibrary = open("./hcaptcha/text.txt").read().splitlines()

        self.payload = {
            "v": self.version,
            "sitekey": "4c672d35-0701-42b2-88c3-78380b0db560"
        }

        self.headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en;q=0.9",
            "Content-Length": "0",
            "Content-Type": "text/plain",
            "Dnt": "1",
            "Origin": "https://newassets.hcaptcha.com",
            "Referer": "https://newassets.hcaptcha.com",
            "Sec-Ch-Ua": "\"Not.A\/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"".replace("114", self.userAgent.split('Chrome/')[1].split('.0.0.0')[0]),
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "Windows",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": self.userAgent
        }
        self.getSetup()

    def getSetup(self):
        self.collEcter = FunctionHsw([1920,1080], self.userAgent)
        self.motionData = MotionData(self.userAgent)

    def getConfig(self):
        resp = self.session.post(
            url = f"https://hcaptcha.com/checksiteconfig?v={self.version}&host=discord.com&sitekey=4c672d35-0701-42b2-88c3-78380b0db560&sc=1&swa=1&spst=0",
            headers = self.headers,
        )
        return resp.json()["c"]

    def getCaptcha(self, c):
        payload = self.payload | {
            "host": "discord.com",
            "hl": "en",
            "a11y_tfe": "true",
            "motionData": dumps(self.motionData.O1()),
            "n": self.collEcter.getToken(c["req"]),
            "c": dumps(c)
        }
        
        self.headers["Content-Type"] = "application/x-www-form-urlencoded"
        self.headers["Content-Length"] = str(len(urlencode(payload)))

        resp = self.session.post(
            url = "https://hcaptcha.com/getcaptcha/4c672d35-0701-42b2-88c3-78380b0db560",
            headers = self.headers,
            data = self.basePayload
        )
        if resp.status_code == 200:
            return resp.json(), resp.cookies["hmt_id"]
        else:
            return None, None

    def solveCaptcha(self, question):
        question = question.lower()
        for i in range(2):
            if f"{question}:yes" in self.textLibrary:
                return {"text": "yes"}
            elif f"{question}:no" in self.textLibrary:
                return {"text": "no"}
            else:
                answer = ""
                for chunk in Solver.create(question + " strictly respond yes or no", None):
                    answer = (answer + chunk).lower()
                if answer.startswith("yes"):
                    with open("./hcaptcha/text.txt", "a") as f:
                        self.solvedAnswers.append(question + ":" + "yes")
                    return {"text": "yes"}
                elif answer.startswith("no"):
                    self.solvedAnswers.append(question + ":" + "no")
                    return {"text": "no"}
                else:
                    continue
                
    def checkCaptcha(self):
        base = self.getCaptcha(self.getConfig())
        if base[0] != None:
            answerList = {}
            for tasks in base[0]["tasklist"]:
                answerList[tasks["task_key"]] = self.solveCaptcha(tasks["datapoint_text"]["en"])

            payload = self.payload | {
                "answers": answerList,
                "c": dumps(dumps(base[0]["c"])), # escape json
                "n": self.collEcter.getToken(base[0]["c"]["req"]), 
                "job_mode": "text_free_entry",
                "motionData": dumps(dumps(self.motionData.O2())), # escape json
                "serverdomain": "discord.com"
            }

            self.headers["Accept"] = "*/*"
            self.headers["Cookie"] = f"hmt_id={base[1]};" # needed cookie
            self.headers["Content-Type"] = "application/json;charset=UTF-8"
            self.headers["Content-Length"] = str(len(payload))

            resp = self.session.post(
                url = f"https://hcaptcha.com/checkcaptcha/4c672d35-0701-42b2-88c3-78380b0db560/{base[0]['key']}",
                headers = self.headers,
                json = payload
            )
            if "pass" in resp.json():
                rest = loads(resp.text)
                if rest["pass"] == True:
                    return resp.json()["generated_pass_UUID"]
                else:
                    return False
            else:
                return False

if __name__  == "__main__":
    from tls_client import Session
    client = Session(
        client_identifier="chrome114",
        random_tls_extension_order=True
    )
    sexxion = Captcha(client, "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    print(sexxion.getConfig())











