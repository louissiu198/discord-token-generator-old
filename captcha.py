from hcaptcha.collectHsw import FunctionHsw
from hcaptcha.motionData import MotionData
from urllib.parse import urlencode
from helper import Utils, Solver
from random import randint, choice
from json import dumps, loads
from time import time, sleep

class Captcha:
    def __init__(self, session, userAgent, opTion, inVite = None):
        self.session = session
        self.userAgent = userAgent
        self.endpoint = choice(["api2.hcaptcha", "hcaptcha"])
        self.version = Utils.getCaptchaV()
        self.solvedAnswers = []
        self.textLibrary = open("./hcaptcha/text.txt", "r").read().splitlines()
        self.inVite = inVite
        self.opTion = opTion
        self.cookie = True

        self.payload = {
            "v": self.version,
            "sitekey": "4c672d35-0701-42b2-88c3-78380b0db560"
        }

        self.headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en;q=0.9",
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
        self.collEcter = FunctionHsw([1920,1080], self.userAgent, self.opTion, self.inVite)
        self.motionData = MotionData(self.userAgent)

    def getConfig(self):
        resp = self.session.post(
            url = f"https://{self.endpoint}.com/checksiteconfig?v={self.version}&host=discord.com&sitekey=4c672d35-0701-42b2-88c3-78380b0db560&sc=1&swa=1&spst=0",
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

        resp = self.session.post(
            url = f"https://{self.endpoint}.com/getcaptcha/4c672d35-0701-42b2-88c3-78380b0db560",
            headers = self.headers,
            data = payload
        )
        if resp.status_code != 429:
            try:
                self.hmt_id = resp.cookies["hmt_id"]
                return resp.json()
            except:
                self.cookie = False
                return resp.json()
        else:
            return None
        # if resp.status_code == 200:
        #     return resp.json(), resp.cookies["hmt_id"]
        # else:
        #     return None, None

    def solveCaptcha(self, question):
        question = question.lower()
        for i in range(2):
            if f"{question}:yes" in self.textLibrary:
                return {"text": "yes"}
            elif f"{question}:no" in self.textLibrary:
                return {"text": "no"}
            else:
                answer = ""
                # Solver.create(session,[{"role": "user", "content": question}])
                for chunk in Solver.create([{"role": "user", "content": question + " strictly respond yes or no"}]):
                    answer = (answer + chunk).lower()
                if answer.startswith("yes"):
                    self.solvedAnswers.append(question + ":" + "yes")
                    return {"text": "yes"}
                elif answer.startswith("no"):
                    self.solvedAnswers.append(question + ":" + "no")
                    return {"text": "no"}
                else:
                    continue
                
    def checkCaptcha(self):
        base = self.getCaptcha(self.getConfig())
        if base != None:
            answerList = {}
            for tasks in base["tasklist"]:
                answerList[tasks["task_key"]] = self.solveCaptcha(tasks["datapoint_text"]["en"])

            payload = self.payload | {
                "answers": answerList,
                "c": dumps(base['c']),
                "n": self.collEcter.getToken(base["c"]["req"]), 
                "job_mode": "text_free_entry",
                "motionData": dumps(self.motionData.O2()),
                "serverdomain": "discord.com"
            }

            self.headers["Accept"] = "*/*"
            if self.cookie == True:
                self.headers["Cookie"] = f"hmt_id={self.hmt_id};" # enable the cookie cause problems
            self.headers["Content-Type"] = "application/json;charset=UTF-8"
            resp = self.session.post(
                url = f"https://{self.endpoint}.com/checkcaptcha/4c672d35-0701-42b2-88c3-78380b0db560/{base['key']}",
                headers = self.headers,
                json = payload
            )
            if "pass" in resp.json():
                rest = loads(resp.text)
                if rest["pass"] == True:
                    for answer in self.solvedAnswers:
                        with open("./hcaptcha/text.txt", "a") as f:
                            f.write(answer + "\n")
                    return resp.json()["generated_pass_UUID"]
                else:
                    for answer in self.solvedAnswers:
                        with open("./hcaptcha/wrong.txt", "a") as f:
                            f.write(answer + "\n")                   
                    return False
            else:
                return False

if __name__  == "__main__":
    from tls_client import Session
    client = Session(
        client_identifier="chrome115",
        random_tls_extension_order=True
    )
    client.proxies = {"http": "http://abduhnvv-rotate:j8n8cp0w4jxr@p.webshare.io:80", "https": "http://abduhnvv-rotate:j8n8cp0w4jxr@p.webshare.io:80"}
    print(client.get("https://api.ipify.org").text)
    while True:
        sexxion = Captcha(client, "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36", 1, None)
        start = time()
        resp = sexxion.checkCaptcha()
        if resp != False and resp != None:
            print(f"Result Cap: {resp[:35]}")
            print(f"Result Time: {time() - start} sec")
        elif resp == None:
            print("Ratelimit")
        elif resp == False:
            print("Solved Error")









