from hcaptcha.collectHsw import FunctionHsw
from hcaptcha.motionData import MotionData
from urllib.parse import urlencode
from random import randint, choice
from httpx import get
from json import dumps
from time import time

import os
from helper import Utils, Completion

INFORMATIONS = {
    "USERAGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "HSWSCRIPT": "https://newassets.hcaptcha.com/c/44fa09c/hsw.js",
    "HAPSCRIPT": "https://hcaptcha.com/1/api.js"
}

class Captcha:
    def __init__(self, session, userAgent):

        self.session = session
        self.version = Utils.findtheVersion()
        self.answers = []
        self.trained = open("./captcha/output/trainedModel.txt").read().splitlines()

    def getSetup(self):
        self.userAgent = get("https://www.whatismybrowser.com/guides/the-latest-user-agent/chrome").text
        self.userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + self.userAgent.split("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/")[1].split(".0.0.0 Safari/537.36")[0] + ".0.0.0 Safari/537.36"
        self.collEcter = FunctionHsw([1900,2000], self.userAgent)
        self.motionData = MotionData(self.userAgent)

    def getConfig(self):
        resp = self.session.post(
            url = "https://hcaptcha.com/checksiteconfig?" + urlencode(self.basePayload),
            headers = self.baseHeaders,
        )
        return resp.json()["c"]

    def getCaptcha(self, c):
        del self.basePayload["sc"]
        del self.basePayload["swa"]
        del self.basePayload["spst"]

        self.basePayload["n"] = self.collEcter.getToken(c["req"]) 
        self.basePayload["c"] = json.dumps(c)
        self.basePayload["hl"] = "en"
        self.basePayload["motionData"] = self.motionData.O1()

        self.baseHeaders["Content-Type"] = "application/x-www-form-urlencoded"
        self.baseHeaders["Content-Length"] = str(len(self.basePayload))

        resp = self.session.post(
            url = "https://hcaptcha.com/getcaptcha/" + "4c672d35-0701-42b2-88c3-78380b0db560",
            headers = self.baseHeaders,
            data = self.basePayload
        ).json()
        try:
            resp["requester_restricted_answer_set"]
        except:
            indexTopic = resp['requester_question']['en']
            if os.path.isdir("./hcaptcha/images/" + indexTopic) == True:
                validPath = True
            else:
                os.mkdir('./hcaptcha/images/'+ indexTopic)
            for i in range(len(resp['requester_question_example'])):
                imageReq =  requests.get(
                    url = str(resp['requester_question_example'][i]),
                    stream = True
                )
                with open("./hcaptcha/images/"+ indexTopic + "/" + str(random.randint(10000000,90000000)) + ".png", 'wb') as f:
                    f.write(imageReq.content)

        self.basePayload["n"] = self.getHsw(resp["c"]["req"])
        self.basePayload["c"] = json.dumps(resp["c"])
        self.basePayload["action"] = "challenge-refresh"
        self.basePayload["old_ekey"] = resp["key"]
        self.basePayload["a11y_tfe"] = "true"
        self.basePayload["extraData"] = resp
        self.basePayload["motionData"] = self.motionData.O2(resp["key"])

        resp = self.session.post(
            url = "https://hcaptcha.com/getcaptcha/" + "4c672d35-0701-42b2-88c3-78380b0db560",
            headers = self.baseHeaders,
            data = self.basePayload
        )
        return resp.json()

    def solveCaptcha(self, question):
        for i in range(2):
            if f"{question.lower()}:yes" in self.trained:
                return {"text": "yes"}
            elif f"{question.lower()}:no" in self.trained:
                return {"text": "no"}
            else:
                answer = ""
                for chunk in Completion.create(question + " strictly respond yes or no", None):
                    answer = (answer + chunk)
                answer = answer.lower()
                if answer.startswith("yes"):
                    with open("./captcha/output/trainedModel.txt", "a") as f:
                        self.answers.append(question.lower() + ":" + "yes")
                    return {"text": "yes"}
                elif answer.startswith("no"):
                    self.answers.append(question.lower() + ":" + "yes")
                    return {"text": "no"}
                else:
                    continue
                
            
    def checkCaptcha(self, extraData):
        del self.basePayload["host"]
        del self.basePayload["action"]
        del self.basePayload["old_ekey"]
        del self.basePayload["a11y_tfe"]
        del self.basePayload["extraData"]

        self.basePayload["motionData"] = self.baseMotion2

        self.baseHeaders["Accept"] = "*/*"
        self.baseHeaders["Content-Type"] = "application/json;charset=UTF-8"
        self.baseHeaders["Content-Length"] = str(len(self.basePayload))

        c = extraData["c"]
        old_ekey = extraData["key"]
        taskList = extraData["tasklist"]
        answerList = {}
        for tasks in taskList:
            answerList[tasks["task_key"]] = self.solveCaptcha(tasks["datapoint_text"]["en"])
        self.basePayload["answers"] = answerList
        self.basePayload["job_mode"] = "text_free_entry"
        self.basePayload["serverdomain"] = self.siteHost

        print(self.basePayload)
        resp = self.session.post(
            url = f"https://hcaptcha.com/checkcaptcha/4c672d35-0701-42b2-88c3-78380b0db560/{old_ekey}",
            headers = self.baseHeaders,
            json = self.basePayload
        )
        if 'pass' in str(resp.json()):
            if resp.json()["pass"] == True:
                for i in range(len(self.answers)):
                    with open("./captcha/output/trainedModel.txt", "a") as f:
                        f.write(self.answers[i] + "\n")
                return resp.json()['generated_pass_UUID']
            elif resp.json()["pass"] == False:
                return False
        else:
            return False
    
    def createTask(self):
        c = self.getConfig()
        g = self.getCaptcha(c)
        f = self.checkCaptcha(g)
        if f != False:
            return f
        else:
            return False
        # except Exception as e:
        #     # print(e)
        #     return False
        
# if __name__ == "__main__":
#     # while True:
#     #     startTime = time.time()
#     #     result = Hcaptcha(siteUrl="https://discord.com/register", siteKey="4c672d35-0701-42b2-88c3-78380b0db560", session=requests.Session()).createTask()
#     #     print(result)
#     #     endTime = time.time() - startTime
#     #     print(round(endTime))
#     resp = requests.get("https://www.google.com/search?q=" + "term").text
#     print(resp)










