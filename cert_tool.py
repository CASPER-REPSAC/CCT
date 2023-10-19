import sys
# from PyQt5.QtWidgets import *
# from PyQt5 import uic
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# form_class = uic.loadUiType("cert_tool_ui.ui")[0]

def crawling(URL, visited, depth=2):
    if depth == 0 or URL in visited:
        return
    
    visited.add(URL)
    
    response = requests.get(URL)
    if response.status_code != 200:
        print(f"{URL} is Skipping: Error Code {response.status_code}")
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
                if URL not in j and 'http://' not in j and 'https://' not in j:
                    j = URL + j
                href_list.append(j)
    for link in href_list:
        if urlparse(link).netloc == urlparse(link).netloc:
            crawling(link, visited, depth-1)
    return href_list
        

# def Check_input(URL):
#     response = urlopen(URL)
#     soup = BeautifulSoup(response, "html.parser")
#     if "<input" in str(soup):
#         return URL
#     else:
#         return ""

# def Is_in_input(URL):
#     href_list = crawling(URL)
#     Ininput = [Check_input(i) for i in href_list]
#     print(Ininput)
    
# class WindowClass(QMainWindow, form_class):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)
#         self.pushButton.clicked.connect(
#             self.functionScan)  # scanbutoon 눌렀을때 연결

#     def functionScan(self):  # scanbutton 눌렀을때 작동
#         URL = self.lineEdit.text()
#         URL_OK = 0
#         try:
#             URL_check = requests.get(URL).status_code  # Response 받아옴
#             # 응답이 200이 아닐때
#             self.label_5.setText(
#                 "plz check URL") if URL_check != 200 else self.label_5.setText("URL is OK")
#             URL_OK = 1
#         except:
#             # 응답을 받는데 에러가 났다
#             self.label_5.setText("plz check URL")
#         if URL_OK:
#             Is_in_input(URL)


# if __name__ == "__main__":
#     # QApplication : 프로그램을 실행시켜주는 클래스
#     app = QApplication(sys.argv)

#     # WindowClass의 인스턴스 생성
#     myWindow = WindowClass()

#     # 프로그램 화면을 보여주는 코드
#     myWindow.show()

#     # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
#     app.exec_()

visited_links = set()
for i in list(crawling('http://github.com/breakpack', visited_links)):
    print(i)