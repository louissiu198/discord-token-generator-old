from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from httpx import get

class FunctionHsw:
    def __init__(self, whList, userAgent, opTion, inVite = None):
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
        self.script = get("https://newassets.hcaptcha.com/c/c2b994f/hsw.js").text
        self.driver = webdriver.Chrome(options=self.options)
        self.prePared(opTion, inVite)

    def prePared(self, choice, invite):
        if choice == 1:
            self.driver.get("https://discord.com/register")
        elif choice == 2:
            self.driver.get("https://discord.com/register")
        elif choice == 3:
            self.driver.get("https://discord.com/invite/" + invite)
    
    def getToken(self, req):
        return self.driver.execute_script(f'{self.script}; return hsw("{req}")')

    def closeConnection(self):
        self.driver.delete_all_cookies()
        self.driver.quit()

if __name__ == "__main__":
    client = FunctionHsw([1920,1080], "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    input()
