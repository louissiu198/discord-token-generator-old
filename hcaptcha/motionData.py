from random import randint, choice, uniform
from json import loads, dumps
from time import time

class MotionData:
    def __init__(self, userAgent):
        self.firstMotion = None
        self.secondMotion = None
        self.userAgent = userAgent
        self.widgetId = "".join([choice("01234567890qwertyuiopasdfghjklzxcvbnm") for i in range(12)])

    @staticmethod
    def formatTime(lists, timestamp):
        start, end = 100, 150
        for i in range(len(lists)):
            lists[i][1] = timestamp + randint(start, end)
            start += 100
            end += 100
        return lists
            
    def O1(self):
        # First GetCaptcha Req [Only 11 Changes] | MM/MP/ETC - Caused by tab and enter (they are not needed) | KU/KUMP/KD/KDMP/WN/WNMP/XY/XYMP - Caused by tab and enter (they are staying static because the xy remains the same as nothing was moved by mouse) 
        timestamp = round(time() * 1000)
        self.firstMotion = {
            "st":timestamp,
            "ku":[[9,timestamp + randint(999,1200)]],
            "ku-mp":0,
            "kd":[[13,timestamp + randint(1999,2200)]],
            "kd-mp":0,
            "v":1,
            "topLevel":{
                "st":timestamp + randint(2999,3200),
                "sc":{
                    "availWidth":1920,"availHeight":1040,"width":1920,"height":1080,"colorDepth":24,"pixelDepth":24,"availLeft":0,"availTop":0,"onchange":None,"isExtended":False
                },
                "nv":{
                    "vendorSub":"","productSub":"20030107","vendor":"Google Inc.","maxTouchPoints":0,"scheduling":{},"userActivation":{},"doNotTrack":None,"geolocation":{},"connection":{},"pdfViewerEnabled":True,"webkitTemporaryStorage":{},"hardwareConcurrency":4,"cookieEnabled":True,"appCodeName":"Mozilla","appName":"Netscape","appVersion":self.userAgent.split("Mozilla/")[1],"platform":"Win32","product":"Gecko","userAgent":self.userAgent,"language":"en-US","languages":["en-US","en"],"onLine":True,"webdriver":False,"bluetooth":{},"clipboard":{},"credentials":{},"keyboard":{},"managed":{},"mediaDevices":{},"storage":{},"serviceWorker":{},"virtualKeyboard":{},"wakeLock":{},"deviceMemory":8,"ink":{},"hid":{},"locks":{},"mediaCapabilities":{},"mediaSession":{},"permissions":{},"presentation":{},"serial":{},"gpu":{},"usb":{},"windowControlsOverlay":{},"xr":{},"userAgentData":{"brands":[{"brand":"Not.A/Brand","version":"8"},{"brand":"Chromium","version":"114"},{"brand":"Google Chrome","version":self.userAgent.split("Chrome/")[1].split(".0.0.0")[0]}],"mobile":False,"platform":"Windows"},
                    "plugins":["internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer"]
                },
                "dr":"",
                "inv":False,
                "exec":False,
                "wn":[[1680,854,2,timestamp + randint(3999,4200)]],
                "wn-mp":0,
                "xy":[[0,0,1,timestamp + randint(4999,5200)]],
                "xy-mp":0,
            },
            "session":[],
            "widgetList":[self.widgetId],
            "widgetId":self.widgetId,
            "href":"https://discord.com/register",
            "prev":{"escaped":False,"passed":False,"expiredChallenge":False,"expiredResponse":False}
        }
        return self.firstMotion
    
    # Reget captcha not needed - payload changed 
    # def O2(self, eKey):
    #     # Second Re-GetCaptcha Req [Only 1 Changes] | Session - from the empty list to append eKey from first req and widgetId
    #     self.firstMotion["session"] = [[eKey, self.widgetId]]
    #     return self.firstMotion
  
    def O2(self):
        # Second CheckCaptcha Req [Only 2 Changes] | KD/KUMP - ku is random number with deciml from 500-700, while kd doesn't changes but timestamp needed to be update
        timestamp = round(time() * 1000)
        mp = uniform(500.9, 610.9)
        du = [[78,1690400237338],[79,1690400237430],[13,1690400237791],[78,1690400238981],[79,1690400239139],[13,1690400239548],[89,1690400241574],[69,1690400241672],[83,1690400241807],[13,1690400242090]]
        self.secondMotion = {
            "st":timestamp,
            "dct":timestamp,
            "kd":MotionData.formatTime(du, timestamp + randint(100,200)),
            "kd-mp":mp,
            "ku":MotionData.formatTime(du, timestamp + randint(200,400)),
            "ku-mp":mp + randint(10,100),
            "topLevel":{
                "st":timestamp + randint(2999,3200),
                "sc":{
                    "availWidth":1920,"availHeight":1040,"width":1920,"height":1080,"colorDepth":24,"pixelDepth":24,"availLeft":0,"availTop":0,"onchange":None,"isExtended":False
                },
                "nv":{
                    "vendorSub":"","productSub":"20030107","vendor":"Google Inc.","maxTouchPoints":0,"scheduling":{},"userActivation":{},"doNotTrack":None,"geolocation":{},"connection":{},"pdfViewerEnabled":True,"webkitTemporaryStorage":{},"hardwareConcurrency":4,"cookieEnabled":True,"appCodeName":"Mozilla","appName":"Netscape","appVersion":self.userAgent.split("Mozilla/")[1],"platform":"Win32","product":"Gecko","userAgent":self.userAgent,"language":"en-US","languages":["en-US","en"],"onLine":True,"webdriver":False,"bluetooth":{},"clipboard":{},"credentials":{},"keyboard":{},"managed":{},"mediaDevices":{},"storage":{},"serviceWorker":{},"virtualKeyboard":{},"wakeLock":{},"deviceMemory":8,"ink":{},"hid":{},"locks":{},"mediaCapabilities":{},"mediaSession":{},"permissions":{},"presentation":{},"serial":{},"gpu":{},"usb":{},"windowControlsOverlay":{},"xr":{},"userAgentData":{"brands":[{"brand":"Not.A/Brand","version":"8"},{"brand":"Chromium","version":"114"},{"brand":"Google Chrome","version":self.userAgent.split("Chrome/")[1].split(".0.0.0")[0]}],"mobile":False,"platform":"Windows"},
                    "plugins":["internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer"]
                },
                "dr":"",
                "inv":False,
                "exec":False,
                "wn":[],
                "wn-mp":0,
                "xy":[],
                "xy-mp":0,
            },
            "v":"1"
        }
        return self.secondMotion

if __name__  == "__main__":
    a = MotionData("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    # print(a.O2())
    x = [[78,1690400237440],[79,1690400237509],[13,1690400237907]]
    MotionData.formatTime(x, round(time()))
    print(x)
    print(round(time()*1000))
