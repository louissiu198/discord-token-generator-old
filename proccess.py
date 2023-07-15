
#!/usr/bin/env python
from tls_client import Session
from helper import Utils
from httpx import get
from json import dumps

class Proccess:
    def __init__(self):
        self.userAgent = Utils.getUseragent()

    def getSession(self):
        self.requestsClient = Session(
            client_identifier = f"chrome{self.userAgent.split('Chrome/')[1].split('.0.0.0')[0]}",
            random_tls_extension_order = True
        )

    def getCookies(self):
        resp = self.requestsClient.get(
            url = "https://discord.com",
            headers = self.headers
        )
        self.__sdcfduid = resp.cookies["__sdcfduid"]
        self.__dcfduid = resp.cookies["__dcfduid"]
        self.__cfruid = resp.cookies["__cfruid"]
    
    def getFingerprint(self):
        # Remove unneeded headers
        del self.headers["Sec-Fetch-User"]
        del self.headers["Upgrade-Insecure-Requests"]
        # Update headers that are here since
        self.headers["Accept"] = "*/*"
        self.headers["Cookie"] = f"__dcfduid={self.__dcfduid}; __sdcfduid={self.__sdcfduid}; __cfruid={self.__cfruid}"
        self.headers["Referer"] = "https://discord.com/register"
        self.headers["Sec-Fetch-Dest"] = "empty"
        self.headers["Sec-Fetch-Mode"] = "cors"
        self.headers["Sec-Fetch-Site"] = "same-origin"
        # Adding new discord x-headers
        self.headers["X-Context-Properties"] = "eyJsb2NhdGlvbiI6IlJlZ2lzdGVyIn0="
        self.headers["X-Debug-Options"] = "bugReporterEnabled"
        self.headers["X-Discord-Locale"] = "en-GB"
        self.headers["X-Discord-Timezone"] = "Asia/Hong_Kong"
        self.headers["X-Super-Properties"] = "eyJvcyI6Ik1hYyBPUyBYIiwiYnJvd3NlciI6IkNocm9tZSIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1HQiIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDEwXzE1XzcpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMTQuMC4wLjAgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjExNC4wLjAuMCIsIm9zX3ZlcnNpb24iOiIxMC4xNS43IiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjIxMDkwMSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0="
        
        self.fingerprint = self.requestsClient.get(
            url = "https://discord.com/api/v9/experiments?with_guild_experiments=true",
            headers = self.headers
        ).json()["fingerprint"]
    
    def getRegister(self):
        while True:
            self.headers = {   
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
                "User-Agent": self.userAgent
            }
            self.captchaKey = None
            if self.captchaKey == None:
                break
            self.getSession()
            self.getCookies()
            self.getFingerprint()
            
            payload = {
                "email": None,
                "invite": None,
                "consent": True,
                "username": Utils.getUsername(),
                "password": Utils.getPassword(),
                "fingerprint": self.fingerprint,
                "captcha_key": self.captchaKey,
                "date_of_birth": Utils.getBirthday(),
                "gift_code_sku_id": None,
                "promotional_email_opt_in": False,
                "unique_username_registration": False
            }

            del self.headers["X-Context-Properties"]
            self.headers["Origin"] = "https://discord.com"
            self.headers["Cookie"] = self.headers["Cookie"] + "; locale=en-GB"
            self.headers["Content-Type"] = "application/json"
            self.headers["X-Fingerprint"] = self.fingerprint

            try:
                resp = self.requestsClient.post(
                    url = "https://discord.com/api/v9/register",
                    headers = self.headers,
                    json = payload
                )
            except Exception as e:
                print(e)
                break

            if resp.status_code == 201:
                self.token = resp.json()["token"]
                print(f"(+) Generated   {self.token}")
            elif "retry_after" in resp.json():
                print(f"(!) RateLimit    {round(resp['retry_after'])}")
            elif "captcha_key" in resp.json() or "captcha_service" in resp.json():
                print(f"(-) Detected    {resp.json()['captcha_key']}")
            else:
                print(f"(-) Exception   {resp.text}")
    
    def getFlagged(self):
        pass




        



