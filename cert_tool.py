import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import requests
from urllib.parse import urlparse, urljoin
from urllib.request import urlopen
from bs4 import BeautifulSoup

form_class = uic.loadUiType("cert_tool_ui.ui")[0]
logfile = open("crawling_log.txt", 'w')
if len(sys.argv) != 2:
    print('How To Use:\npython cert_tool.py {cheat sheet PATH}')
    sys.exit()
sheet_path = sys.argv[1]
Cheat_sheet = open(sheet_path, 'r')
Xss_q = Cheat_sheet.readlines()
def crawling(URL, visited, depth=2):
    if depth == 0 or URL in visited:
        return
    
    visited.add(URL)
    
    try :
        response = requests.get(URL)
        if response.status_code != 200:
            print(f"[-]{URL} is Skipping: Error Code {response.status_code}")
            return
        
        soup = BeautifulSoup(response.text, "html.parser")
        tag_a_list = [i.split()
                    for i in str(soup).splitlines() if "<a" in i.split()]
        href_list = []  # href만 빼내기
        for i in tag_a_list:
            for j in i:
                if "href=" in j:
                    j = j.replace('href=\"', '')
                    j = j[:j.find('\"')]
                    j = j.replace('amp;','')
                    j = urljoin(URL, j)
                    href_list.append(j)
        for link in href_list:
            logfile.write(f"[+]current crawling: {link}")
            logfile.write('\n')
            print(f"[+]current crawling: {link}")
            if urlparse(link).netloc == urlparse(link).netloc:
                crawling(link, visited, depth-1)
    except Exception as e:
        logfile.write(f"[-]Connect Error: {e}")
        logfile.write('\n')
        print(f"[-]Connect Error: {e}")        

logfile2 = open("check_input_log.txt", 'w')
def Check_input(link):
    print(f"[+]check input : {link}")
    try:
        response = requests.get(link)
        if response.status_code != 200:
            logfile2.write(f"[-]{link} is Skipping: Error Code {response.status_code}")
            logfile2.write('\n')
            print(f"[-]{link} is Skipping: Error Code {response.status_code}")
            return ''
        soup = BeautifulSoup(response.text, "html.parser")
        if "type=\"text\"" in str(soup) or "<textarea" in str(soup):
            return link
    except Exception as e:
        logfile2.write(f"[-]Connect Error: {e}")
        logfile2.write('\n')
        print(f"[-]Connect Error: {e}")

def Is_in_input(URL):
    visited_links = set()
    crawling(URL, visited_links)
    print(f"[*] In input test start")
    logfile2.write(f"[*] In input test start")
    logfile2.write('\n')
    In_input = [ j for j in [Check_input(i) for i in visited_links] if j != False]
    logfile2.write(f"In input list : {In_input}")
    return In_input

def Attack(URL):
    Des_URL_list = Is_in_input(URL)
    print("parse OK", Des_URL_list)
    for url in Des_URL_list:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            form_tag = soup.find('form')
            if form_tag:
                action_url = form_tag.get('action')
                print("Form의 action URL:", action_url)
            else:
                print("폼이 없거나 action 속성이 없습니다.")
        else:
            print("페이지에 접근할 수 없습니다. 응답 코드:", response.status_code)
        input_tags = soup.find_all('input')
        input_names = [input_tag.get('name') for input_tag in input_tags]
        area_tags = soup.find_all('textarea')
        area_names = [input_tag.get('name') for input_tag in input_tags]
        print(input_names, area_names)

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(
            self.functionScan)  # scanbutoon 눌렀을때 연결

    def functionScan(self):  # scanbutton 눌렀을때 작동
        logfile.write("gui Start")
        logfile.write('\n')
        URL = self.lineEdit.text()
        URL_OK = 0
        try:
            URL_check = requests.get(URL).status_code  # Response 받아옴
            # 응답이 200이 아닐때
            self.label_5.setText(
                "plz check URL") if URL_check != 200 else self.label_5.setText("URL is OK")
            URL_OK = 1
        except:
            # 응답을 받는데 에러가 났다
            self.label_5.setText("plz check URL")
        if URL_OK:
            Attack(URL)


if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()

logfile.close()