import sys
import requests
from urllib.parse import urlparse, urljoin
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.alert import Alert

logfile = open("crawling_log.txt", 'w')
if len(sys.argv) != 2:
    print('How To Use:\npython cert_tool.py {cheat sheet PATH}')
    sys.exit()
sheet_path = sys.argv[1]
Cheat_sheet = open(sheet_path, 'r')

def crawling(url, URL, visited, depth=2):
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
            if urlparse(link).netloc == urlparse(link).netloc == urlparse(url).netloc:
                crawling(url, link, visited, depth-1)
    except Exception as e:
        logfile.write(f"[-]Connect Error: {e}")
        logfile.write('\n')
        print(f"[-]Connect Error: {e}")        

def crwaling2(URL, url, visited_links=None):
    if visited_links is None:
        visited_links = set()
    
    # URL에 접근
    response = requests.get(url)
    
    if response.status_code == 200:
        # HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # 현재 URL을 방문한 것으로 표시
        visited_links.add(url)

        # 모든 링크 가져오기
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            absolute_url = urljoin(url, href)
            # 상대 URL을 절대 URL로 변환
            
            # 같은 도메인 내의 URL만 고려 (다른 도메인으로의 이동 방지)
            if urlparse(absolute_url).netloc == urlparse(url).netloc == urlparse(URL).netloc:
                if absolute_url not in visited_links:
                    visited_links.update(crwaling2(URL, absolute_url, visited_links))
    return visited_links


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
    crawling(URL, URL, visited_links)
    print(f"[*] In input test start")
    logfile2.write(f"[*] In input test start")
    logfile2.write('\n')
    In_input = [ j for j in [Check_input(i) for i in visited_links] if j != False]
    logfile2.write(f"In input list : {In_input}")
    return In_input

driver = webdriver.Chrome()
def Alert_check(URL):
    print(f'[+]재크롤링 시작')
    Des_URL_list = crwaling2(URL, URL)
    for i in Des_URL_list:
        print(f'- {i}')
    result = []
    for URL in list(set(Des_URL_list)):
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        absolute_links = set()
        for link in links:
            href = link.get('href')
            absolute_url = urljoin(URL, href)
            absolute_links.add(absolute_url)
        for link in absolute_links:
            print('[+]alert확인 link :', link)
            try:
                driver.get(link)
                try:
                    alert = driver.switch_to.alert
                    alert_text = alert.text
                    print("[++]Alert 텍스트:", alert_text)
                    # 필요한 작업 수행 (예: 확인 버튼 클릭)
                    alert.accept()
                    result.append(link)
                except:
                    print("[-]알림이 없거나 처리할 수 없습니다.")
            except:
                print('[-]error')         
    return result

Xss_q = Cheat_sheet.readlines()
def Attack(URL):
    Des_URL_list = Is_in_input(URL)
    for i in Des_URL_list:
        if(i == None):
            Des_URL_list.remove(i)
    print("[+]parse OK\n", Des_URL_list)
    for url in Des_URL_list:
        print(f'[+]form 유무 검사: {url}')
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            form_tag = soup.find('form')
            if form_tag:
                action_url = form_tag.get('action')
                print("[+]Form의 action URL:", action_url)
            else:
                print("[-]폼이 없거나 action 속성이 없습니다.")
                continue
        else:
            print("[-]페이지에 접근할 수 없습니다. 응답 코드:", response.status_code)
            continue
        
        input_tags = soup.find_all('input')
        input_names = [input_tag.get('name') for input_tag in input_tags]
        area_tags = soup.find_all('textarea')
        area_names = [area_tag.get('name') for area_tag in area_tags]
        
        form_data = []
        for payload in Xss_q:
            data = {}
            for input_name in input_names:
                data[input_name] = "certtest"
            for area_name in area_names:
                data[area_name] = payload
            form_data.append(data)
        print('[*]form_data:', form_data)
        
        for data_form in form_data:
            target_url = urljoin(url, action_url)

            print("[+]target_url:", target_url)
            response_req = requests.post(target_url, data=data_form)
            if response_req.status_code == 200:
                print('[+]폼 제출성공')
            else:
                print('[-]폼 제출실패')
    print('[*]ALERT가 확인되는 URL: ', Alert_check(URL))

def functionScan(URL):  # scanbutton 눌렀을때 작동
    logfile.write("gui Start")
    logfile.write('\n')
    URL_OK = 0
    try:
        URL_check = requests.get(URL).status_code  # Response 받아옴
        # 응답이 200이 아닐때
        print('url is not available') if URL_check != 200 else print("URL is OK")
        URL_OK = 1
    except:
        # 응답을 받는데 에러가 났다
        print("plz check URL")
    if URL_OK:
        Attack(URL)
        driver.quit()

url = input('url?')
functionScan(url)
logfile.close()
logfile2.close()