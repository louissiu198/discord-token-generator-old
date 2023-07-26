import imap_tools
from httpx import get
import base64
import random
import re

class Gmail:
    def __init__(self, email):
        self.real = str(email.split(":")[0])
        self.email = str(email.split("@")[0]) + "+"
        self.password = str(email.split(":")[1])

    def getGenerate(self):
        while True:
            randomList = "qwertyuiopasdfghjklzxcvbnm"
            self.geneRated = self.email + "".join([random.choice(randomList) for i in range(6)]) + "@outlook.com"
            gmailList = open("./gmail/gmail.txt").read().splitlines()
            if self.geneRated in gmailList:
                continue
            else:
                with open("./gmail/gmail.txt", "a") as f:
                    f.write(self.geneRated + "\n")
                return self.geneRated
            
            
    def getRecieve(self):
        bracket = []
        with imap_tools.MailBox('outlook.office365.com','993').login(self.real,self.password,'INBOX') as mailbox:
            for messages in mailbox.fetch():
                print(messages)

                # if messages.from_ == 'krunker030@gmail.com':
                #     if messages.to == self.geneRated:
                #         website = messages.html

                #         # website = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', website)
                #         # for i in range(len(website)):
                #         #     if website[i].startswith("https://click.discord.com/ls/click?upn="):
                #         #         bracket.append(website[i])
                #         mailbox.delete(messages.uid)
                #         return website
                
    def getVerify(self, bracket):
        resp = get(
            url = bracket[1], 
            follow_redirects = True
        ).url
        return resp.split('https://discord.com/verify#token=')[1]
