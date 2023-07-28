
#!/usr/bin/env python
from tls_client import Session
from captcha import Captcha
from secrets import token_urlsafe
from helper import Utils
from httpx import get
from json import dumps
from time import time

unlocked = 0
disabled = 0
flagged = 0
locked = 0

unverfied = False
uncreated = True
joinserver = False

inviteKey = ""

class Proccess:
    def __init__(self):
        self.userAgent = Utils.getUseragent()

    def getCookies(self):
        if unverfied:
            discord = "https://discord.com/register"
        elif uncreated:
            discord = "https://discord.com"
        elif joinserver:
            discord = "https://discord.com/invite/" + inviteKey

        resp = self.requestsClient.get(
            url = discord,
            headers = self.headers
        )
        self.__sdcfduid = resp.cookies["__sdcfduid"]
        self.__dcfduid = resp.cookies["__dcfduid"]
        self.__cfruid = resp.cookies["__cfruid"]
    
    def getFingerprint(self):
        # # Remove unneeded headers
        # del self.headers["Sec-Fetch-User"]
        # del self.headers["Upgrade-Insecure-Requests"]
        # # Update headers that are here since
        # self.headers["Accept"] = "*/*"
        # self.headers["Cookie"] = f"__dcfduid={self.__dcfduid}; __sdcfduid={self.__sdcfduid}; __cfruid={self.__cfruid}; locale=en-GB"
        # self.headers["Sec-Fetch-Dest"] = "empty"
        # self.headers["Sec-Fetch-Mode"] = "cors"
        # self.headers["Sec-Fetch-Site"] = "same-origin"
        # # Adding new discord x-headers
        # if unverfied:
        #     self.headers["Referer"] = "https://discord.com/register"
        #     self.headers["X-Context-Properties"] = "eyJsb2NhdGlvbiI6IlJlZ2lzdGVyIn0="
        #     self.headers["X-Debug-Options"] = "bugReporterEnabled"
        #     self.headers["X-Discord-Locale"] = "en-GB"
        #     self.headers["X-Discord-Timezone"] = "Asia/Hong_Kong"
        #     self.headers["X-Super-Properties"] = "eyJvcyI6Ik1hYyBPUyBYIiwiYnJvd3NlciI6IkNocm9tZSIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1HQiIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDEwXzE1XzcpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMTQuMC4wLjAgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjExNC4wLjAuMCIsIm9zX3ZlcnNpb24iOiIxMC4xNS43IiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjIxMDkwMSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0="
        #     experiments = "https://discord.com/api/v9/experiments?with_guild_experiments=true"
        # elif uncreated:
        #     self.headers["Referer"] = "https://discord.com/"
        #     self.headers["X-Track"] = "eyJvcyI6Ik1hYyBPUyBYIiwiYnJvd3NlciI6IkNocm9tZSIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1HQiIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDEwXzE1XzcpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMTQuMC4wLjAgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjExNC4wLjAuMCIsIm9zX3ZlcnNpb24iOiIxMC4xNS43IiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjk5OTksImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9"
        #     experiments = "https://discord.com/api/v9/experiments"
        # elif joinserver:
        #     pass
        
        # self.fingerprint = self.requestsClient.get(
        #     url = experiments,
        #     headers = self.headers
        # ).json()["fingerprint"]
        self.fingerprint = str((int(time()*1000) - 1420070400000) << 22) + "." + token_urlsafe(20)

    def getRegister(self):
        # while True:
        self.headers = Utils.getHeaders(self.userAgent)
        self.requestsClient = Session(
            client_identifier = f"chrome{self.userAgent.split('Chrome/')[1].split('.0.0.0')[0]}",
            random_tls_extension_order = True
        )
        self.captchaKey = Captcha(self.requestsClient, self.userAgent, 1, None)
        if self.captchaKey == None or self.captchaKey == False:
            # break
            print("captcha solver wrong")
        else:
            print(self.captchaKey[:35])
        
        self.getCookies()
        self.getFingerprint()
        
        payload = {
            "consent":True,
            "fingerprint":self.fingerprint,
            "username":Utils.getUsername(),
            "captcha_key":str(self.captchaKey),
        }
        if unverfied:
            payload = payload | {
                "email": None,
                "invite": None,
                "password": Utils.getPassword(),
                "global_name": "",
                "date_of_birth": Utils.getBirthday(),
                "gift_code_sku_id": None,
                "promotional_email_opt_in": False,
                "unique_username_registration": False
            }
            del self.headers["X-Context-Properties"]
            self.headers["X-Captcha-Key"] = self.captchaKey
        elif uncreated:
            self.headers["X-Track"] = "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLUdCIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExNS4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTE1LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwLjE1LjciLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6OTk5OSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0="
        if joinserver:
            payload = payload | {
                "invite": inviteKey
            }
        self.headers["Origin"] = "https://discord.com"
        self.headers["Content-Type"] = "application/json"
        self.headers["X-Fingerprint"] = self.fingerprint
        print(self.headers)
        print(self.payload)
        # try:
        resp = self.requestsClient.post(
            url = "https://discord.com/api/v9/register",
            headers = self.headers,
            json = payload
        )
        print(resp.text)
        # except Exception as e:
        #     print(e)
            # break
        if resp.status_code == 201:
            self.token = resp.json()["token"]
            print(f"(*) Generated   {self.token}")
        elif "retry_after" in resp.text:
            print(f"(^) RateLimit    {round(resp['retry_after'])}")
        elif "captcha_key" in resp.text or "captcha_service" in resp.text:
            print(f"(&) Detected    {resp.json()['captcha_key']}")
        else:
            print(f"(-) Exception   {resp.text}")
    
    def getFlagged(self):
        pass

if __name__ == "__main__":
    client = Proccess()
    client.getRegister()



