import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup

form_class = uic.loadUiType("cert_tool_ui.ui")[0]

def crawling(URL):
    response = urlopen(URL)
    soup = BeautifulSoup(response, "html.parser")
    tag_a_list = [i.split() for i in str(soup).splitlines() if "<a" in i.split()]
    href_list = [] #href만 빼내기
    for i in tag_a_list:
        for j in i:
            if "href=" in j:
                j = j[j.find("=")+2:j.find("\"", j.find("=")+2, len(j))]
                if "https" not in j or "http" not in j:
                    j = URL + j                    
                if j != "#" or len(j) > 1 or URL not in j:
                    href_list.append(j)
    href_list = list(set(href_list))

class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.functionScan) #scanbutoon 눌렀을때 연결
        
    def functionScan(self): #scanbutton 눌렀을때 작동
        URL = self.lineEdit.text()
        URL_OK = 0
        try:
            URL_check = requests.get(URL).status_code #Response 받아옴
            #응답이 200이 아닐때
            self.label_5.setText("plz check URL") if URL_check != 200 else self.label_5.setText("URL is OK")
            URL_OK = 1
        except:
            #응답을 받는데 에러가 났다
            self.label_5.setText("plz check URL")
        if URL_OK:
            crawling(URL)
            
    
    
        
if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()