import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import requests
from urllib.parse import urlparse, urljoin
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.alert import Alert

Des_URL_list =  ['http://localhost/tem/index.php', 'http://localhost/board/freeboardwrite.php']
for url in Des_URL_list:
    
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        form_tag = soup.find('form')
        if form_tag:
            action_url = form_tag.get('action')
            print("[+]Form의 action URL:", action_url)
        else:
            print("[-]폼이 없거나 action 속성이 없습니다.")
    else:
        print("[-]페이지에 접근할 수 없습니다. 응답 코드:", response.status_code)
        break     