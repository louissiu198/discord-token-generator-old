from hcaptcha.collectHsw import FunctionHsw
from hcaptcha.motionData import MotionData
from urllib.parse import urlencode
from helper import Utils, Solver
from random import randint, choice
from json import dumps, loads
from time import time, sleep
import json
import os

class Captcha:
    def __init__(self, session, userAgent, opTion, inVite = None):
        self.session = session
        self.userAgent = userAgent
        self.version = Utils.getCaptchaV()
        self.solvedAnswers = []
        self.textLibrary = open("./hcaptcha/text.txt", "r").read().splitlines()
        self.inVite = inVite
        self.opTion = opTion

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

        resp = self.session.post(
            url = "https://hcaptcha.com/getcaptcha/4c672d35-0701-42b2-88c3-78380b0db560",
            headers = self.headers,
            data = payload
        )
        if resp.status_code == 200:
            return resp.json(), resp.cookies["hmt_id"]
        else:
            return None, None

    def solveCaptcha(self, question):
        question = question.lower()
        print(question)
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
        if base[0] != None:
            answerList = {}
            for tasks in base[0]["tasklist"]:
                answerList[tasks["task_key"]] = self.solveCaptcha(tasks["datapoint_text"]["en"])

            payload = self.payload | {
                "answers": answerList,
                # "c": "{\"type\":\"hsw\",\"req\":\"hellow\"}".replace("hellow", dumps(base[0]['c']['req'])), # escape json
                "c": dumps(base[0]['c']),
                "n": self.collEcter.getToken(base[0]["c"]["req"]), 
                "job_mode": "text_free_entry",
                "motionData": dumps(self.motionData.O2()),
                # "motionData": '{"st":1690400235610,"dct":1690400235610,"kd":[[78,1690400237338],[79,1690400237430],[13,1690400237791],[78,1690400238981],[79,1690400239139],[13,1690400239548],[89,1690400241574],[69,1690400241672],[83,1690400241807],[13,1690400242090]],"kd-mp":528,"ku":[[78,1690400237440],[79,1690400237509],[13,1690400237907],[78,1690400239100],[79,1690400239231],[13,1690400239636],[89,1690400241664],[69,1690400241786],[83,1690400241966],[13,1690400242197]],"ku-mp":528.5555555555555,"topLevel":{"st":1690400225774,"sc":{"availWidth":1680,"availHeight":933,"width":1680,"height":1050,"colorDepth":30,"pixelDepth":30,"availLeft":0,"availTop":25,"onchange":null,"isExtended":false},"nv":{"vendorSub":"","productSub":"20030107","vendor":"Google Inc.","maxTouchPoints":0,"scheduling":{},"userActivation":{},"doNotTrack":null,"geolocation":{},"connection":{},"pdfViewerEnabled":true,"webkitTemporaryStorage":{},"hardwareConcurrency":8,"cookieEnabled":true,"appCodeName":"Mozilla","appName":"Netscape","appVersion":"5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36","platform":"MacIntel","product":"Gecko","userAgent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36","language":"en-GB","languages":["en-GB","en-US","en"],"onLine":true,"webdriver":false,"bluetooth":{},"clipboard":{},"credentials":{},"keyboard":{},"managed":{},"mediaDevices":{},"storage":{},"serviceWorker":{},"virtualKeyboard":{},"wakeLock":{},"deviceMemory":8,"ink":{},"hid":{},"locks":{},"mediaCapabilities":{},"mediaSession":{},"permissions":{},"presentation":{},"serial":{},"gpu":{},"usb":{},"windowControlsOverlay":{},"xr":{},"userAgentData":{"brands":[{"brand":"Not.A/Brand","version":"8"},{"brand":"Chromium","version":"114"},{"brand":"Google Chrome","version":"114"}],"mobile":false,"platform":"macOS"},"plugins":["internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer"]},"dr":"","inv":false,"exec":false,"wn":[],"wn-mp":0,"xy":[],"xy-mp":0},"v":1}',
                "serverdomain": "discord.com"
            }

            self.headers["Accept"] = "*/*"
            self.headers["Cookie"] = f"hmt_id={base[1]};" # needed cookie
            self.headers["Content-Type"] = "application/json;charset=UTF-8"
            print(self.headers)
            print(payload)
            resp = self.session.post(
                url = f"https://hcaptcha.com/checkcaptcha/4c672d35-0701-42b2-88c3-78380b0db560/{base[0]['key']}",
                headers = self.headers,
                json = payload
            )
            print(resp.text)
            if "pass" in resp.json():
                rest = loads(resp.text)
                if rest["pass"] == True:
                    for answer in self.solvedAnswers:
                        with open("./hcaptcha/text.txt", "a") as f:
                            f.write(answer + "\n")
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
    sexxion = Captcha(client, "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36", 1, None)
    print(sexxion.checkCaptcha())










