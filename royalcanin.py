import oracledb
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
}
browser = webdriver.Chrome()
browser.maximize_window()


# # DB 연결
# conn = oracledb.connect(user="ora_user", password="1111", dsn="localhost:1521/xe")
# cursor = conn.cursor()

for page in range(1, 6):
    url = f"https://www.royalcanin.com/kr/dogs/products/retail-products?page={page}"
    browser.get(url)
    time.sleep(2)

    soup = BeautifulSoup(browser.page_source, "lxml")
    basic_list = soup.find("ul", {"class": "sc-gweoQa jMdvrK product-grid"})

    if not basic_list:
        print(f"Page {page}: 제품 그리드를 찾을 수 없습니다.")
        continue
    
    feed_list = basic_list.find_all("li")
    print(f"Page {page}: Found {len(feed_list)} feeds.")
    
    for i, feed in enumerate(feed_list):
        
        info_class = feed.find("div", {"class": "sc-klVQfs bsHeaI"})
        if info_class:
            title = info_class.find("h2").text.strip()
            kind = info_class.find("p").text.strip()
            img = feed.find("img")["src"]
            
            # 파일 저장
            with open(f"royalcanin_{page}_{i+1}.jpg", "wb") as f:
                d_img = requests.get(img)
                f.write(d_img.content)
            
            print(f"[번호 {i+1}]")
            print("사료명: ", title)
            print("종류: ", kind)
            print("이미지: ", img)
            
            # 개별 링크로 들어가기
            link = "https://www.royalcanin.com"+feed.find("a")["href"]
            browser.get(link)
            time.sleep(3)
            browser.execute_script("window.scrollTo(0,700)")
            time.sleep(1)
            
            try:
                elem = browser.find_element(By.XPATH,'//*[@id="__next"]/main/div[2]/div[1]/div[2]/div[4]/div[2]/div/button')
                elem.click()
                time.sleep(2)
                
                elem2 = browser.find_element(By.XPATH,'//*[@id="__next"]/main/div[2]/div[1]/div[2]/div[4]/div[2]/div/div/div[1]/div/button')
                elem2.click()
                time.sleep(2)
                
                soup2 = BeautifulSoup(browser.page_source, "lxml")
                
                p_infobox = soup2.find("div",{"class":"sc-fPXMVe eITAxU"}).text
                
                if p_infobox:
                    # 삭제할 문구 정의
                    
                    info = p_infobox.strip().replace('"','').replace('서,','')
                    text_list = info.split(',')
            
                    print("사료 성분: ",info)
                    print("사료 성분 개수: ",len(text_list))
                    print("-" * 70)
            except:
                print("오류발생")

        #     # DB 저장
        #     sql = "insert into daum_movie values (movie_seq.nextval, :1, :2, :3, :4)"
        #     cursor.execute(sql, (title, img, kind, ''))
        #     cursor.execute('commit')
        # else:
        #     print(f"Page {page}, Feed {i+1}: info_class with expected class name not found.")

            # 다시 이전 창으로 돌아가기
            browser.back()
            time.sleep(2)
    
   
print("종료")
# cursor.close()
# conn.close()
browser.quit()
