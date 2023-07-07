from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from httpx import get

class FunctionHsw:
    def __init__(self, whList, userAgent):
        self.options = Options()
        self.options.add_argument("--headless") 
        self.options.add_argument("--incognito")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--single-process")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("disable-infobars")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_experimental_option("useAutomationExtension", False)
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.script = get("")
        self.driver = webdriver.Chrome(options=self.options)
        self.prePared()

    def prePared(self):
        self.driver.get("https://discord.com/register")
    
    def getToken(self, req):
        return self.driver.execute_script(f"{self.script}; return hsw('{req}')")

    def closeConnection(self):
        self.driver.delete_all_cookies()
        self.driver.quit()
