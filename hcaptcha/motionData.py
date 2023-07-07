import requests
import random
import json
import time

class MotionData:
    def __init__(self, userAgent):
        self.firstMotion = None
        self.secondMotion = None
        self.thirdMotion = None
        self.calledTimes = 0
        self.userAgent = userAgent
        self.widgetId = "".join([random.choice("01234567890qwertyuiopasdfghjklzxcvbnm") for i in range(12)])

    @staticmethod
    def formatTime(lists, timestamp):
        start, end = 100, 150
        for i in range(len(lists)):
            lists[i][1] = timestamp + random.randint(start, end)
            start += 100
            end += 100
            
    def O1(self):
        # First GetCaptcha Req [Only 11 Changes] | MM/MP/ETC - Caused by tab and enter (they are not needed) | KU/KUMP/KD/KDMP/WN/WNMP/XY/XYMP - Caused by tab and enter (they are staying static because the xy remains the same as nothing was moved by mouse) 
        timestamp = round(time.time() * 1000)
        self.firstMotion = {
            "st":timestamp,
            "ku":[[9,timestamp + random.randint(999,1200)]],
            "ku-mp":0,
            "kd":[[13,timestamp + random.randint(1999,2200)]],
            "kd-mp":0,
            "v":1,
            "topLevel":{
                "st":timestamp + random.randint(2999,3200),
                "sc":{
                    "availWidth":1920,"availHeight":1040,"width":1920,"height":1080,"colorDepth":24,"pixelDepth":24,"availLeft":0,"availTop":0,"onchange":None,"isExtended":False
                },
                "nv":{
                    "vendorSub":"","productSub":"20030107","vendor":"Google Inc.","maxTouchPoints":0,"scheduling":{},"userActivation":{},"doNotTrack":None,"geolocation":{},"connection":{},"pdfViewerEnabled":True,"webkitTemporaryStorage":{},"hardwareConcurrency":4,"cookieEnabled":True,"appCodeName":"Mozilla","appName":"Netscape","appVersion":self.userAgent.split("Mozilla/"),"platform":"Win32","product":"Gecko","userAgent":self.userAgent,"language":"en-US","languages":["en-US","en"],"onLine":True,"webdriver":False,"bluetooth":{},"clipboard":{},"credentials":{},"keyboard":{},"managed":{},"mediaDevices":{},"storage":{},"serviceWorker":{},"virtualKeyboard":{},"wakeLock":{},"deviceMemory":8,"ink":{},"hid":{},"locks":{},"mediaCapabilities":{},"mediaSession":{},"permissions":{},"presentation":{},"serial":{},"gpu":{},"usb":{},"windowControlsOverlay":{},"xr":{},"userAgentData":{"brands":[{"brand":"Not.A/Brand","version":"8"},{"brand":"Chromium","version":"114"},{"brand":"Google Chrome","version":self.userAgent.split("Chrome/")[1].split(".0.0.0")[0]}],"mobile":False,"platform":"Windows"},
                    "plugins":["internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer"]
                },
                "dr":"",
                "inv":False,
                "exec":False,
                "wn":[[613,969,1,timestamp + random.randint(3999,4200)]],
                "wn-mp":0,
                "xy":[[0,0,1,timestamp + random.randint(4999,5200)]],
                "xy-mp":0,
            },
            "session":[],
            "widgetList":[self.widgetId],
            "widgetId":self.widgetId,
            "href":"https://discord.com/register",
            "prev":{"escaped":False,"passed":False,"expiredChallenge":False,"expiredResponse":False}
        }
        return self.firstMotion
        
    def O2(self, eKey):
        # Second GetCaptcha Req [Only 1 Changes] | Session - from the empty list to append eKey from first req and widgetId
        self.firstMotion["session"] = [[eKey, self.widgetId]]
        return self.firstMotion
  
    def O3(self):
        # Third CheckCaptcha Req [Only 2 Changes] | KD/KUMP - ku is random number with deciml from 500-700, while kd doesn't changes but timestamp needed to be update
        timestamp = round(time.time() * 1000)
        self.secondMotion = {
            "st":timestamp,
            "dct":timestamp,
            "kd":self.formatTime([[78,1688133650697],[79,1688133650792],[13,1688133651105],[89,1688133653675],[69,1688133653819],[83,1688133654004],[13,1688133654353],[89,1688133656152],[69,1688133656264],[83,1688133656451],[13,1688133656768]], timestamp),
            "kd-mp":random.uniform(500.9, 610.9),
            "ku":self.formatTime([[78,1688133650816],[79,1688133650928],[13,1688133651225],[89,1688133653804],[69,1688133653939],[83,1688133654130],[13,1688133654457],[89,1688133656288],[69,1688133656385],[83,1688133656587],[13,1688133657558]], timestamp + 1000),
            "ku-mp":random.uniform(560.9, 690.9),
            "v":1,
            "topLevel":{
                "st":timestamp + random.randint(2999,3200),
                "sc":{
                    "availWidth":1920,"availHeight":1040,"width":1920,"height":1080,"colorDepth":24,"pixelDepth":24,"availLeft":0,"availTop":0,"onchange":None,"isExtended":False
                },
                "nv":{
                    "vendorSub":"","productSub":"20030107","vendor":"Google Inc.","maxTouchPoints":0,"scheduling":{},"userActivation":{},"doNotTrack":None,"geolocation":{},"connection":{},"pdfViewerEnabled":True,"webkitTemporaryStorage":{},"hardwareConcurrency":4,"cookieEnabled":True,"appCodeName":"Mozilla","appName":"Netscape","appVersion":self.userAgent.split("Mozilla/"),"platform":"Win32","product":"Gecko","userAgent":self.userAgent,"language":"en-US","languages":["en-US","en"],"onLine":True,"webdriver":False,"bluetooth":{},"clipboard":{},"credentials":{},"keyboard":{},"managed":{},"mediaDevices":{},"storage":{},"serviceWorker":{},"virtualKeyboard":{},"wakeLock":{},"deviceMemory":8,"ink":{},"hid":{},"locks":{},"mediaCapabilities":{},"mediaSession":{},"permissions":{},"presentation":{},"serial":{},"gpu":{},"usb":{},"windowControlsOverlay":{},"xr":{},"userAgentData":{"brands":[{"brand":"Not.A/Brand","version":"8"},{"brand":"Chromium","version":"114"},{"brand":"Google Chrome","version":self.userAgent.split("Chrome/")[1].split(".0.0.0")[0]}],"mobile":False,"platform":"Windows"},
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
