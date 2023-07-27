# Discord Token Generator

Hi guys, I think in this moment I have already released this api or library or source code
First, please leave a star or donate money to support me
Therefore I hope you guys weren't skidding my gen or others
So today I'm gonna teach you how to make a discord token generator

### Step 1
```
Requirements
+ Python                            REQUIRED
+ Http Toolkit (some intercepter)   NOT-REQUIRED
```
1. If you have toolkit then start interception if no then (option + command + i) or (command + key + i) then switch to network bar
2. Go to discord.com or discord.com/register
3. Register an account and do other actions
4. Go on network bar and check what requests you sent to discord

### Step 2
1. Use the network bar on the first step and go on search bar type in hcaptcha (needed)
2. Check what hcaptcha sent and recieve, XML reqs for total should be 2,3 depends on the methods (image, text)
3. For text skip the second 'getcaptcha' requests when you write it in python and add the special param "a11y_tfe"
4. Then hmm ........ write the whole code out
5. Captcha solver would be finished ...

### Step 3
1. Use the network bar on the first step and go on search bar type in discord (needed)
2. Re-build the needed reqs, 'fingerprint', 'register', 'verify' and get needed cookies
3. Write it in python using tls_client, its a library in http2 which is way faster than requests and also undetected because of tls 
