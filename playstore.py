# 모듈 import
import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pandas as pd
# 옵션 설정
# 2-1 드라이버 옵션 설정
chrome_option = webdriver.ChromeOptions()
chrome_option.add_experimental_option('detach', True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_option)

# 3. 브라우저 띄우기
driver.maximize_window()
driver.get('https://play.google.com/store/apps/details?id=com.campmobile.snow&hl=ko')
time.sleep(3)


# 4. 리뷰 팝업창 띄우기
# 팝업 버튼 클릭
# driver.find_element(By.XPATH,'//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[2]/div/div[1]/'
#                              'c-wiz[4]/section/header/div/div[2]/button/i').click()
driver.find_element(By.XPATH,'/html/body/c-wiz[2]/div/div/div/div[2]/div/div[1]/div[1]'
                             '/c-wiz[4]/section/header/div/div[2]/button').click()

# 팝업창 활성화(스크롤을 움직이기 위해)
popup = driver.find_element(By.CLASS_NAME, 'fysCi')
popup.click()

prev_count = 0
new_count = 0


# 리뷰 확보
while True:
    driver.find_element(By.TAG_NAME,'body').send_keys(Keys.END)
    time.sleep(3)
    new_count = len(driver.find_elements(By.CLASS_NAME, 'h3YV2d'))

    if prev_count == new_count or new_count > 2000:
        break
    prev_count = new_count

stars = driver.find_elements(By.CLASS_NAME, 'iXRFPc')
reviews = driver.find_elements(By.CLASS_NAME, 'h3YV2d')
print(reviews)
review_list = []
for temp in reviews:
    review_list.append(temp.text)

stars_list = []
for temp in stars:
    temp = temp.get_attribute('aria-label')
    temp = temp.replace('별표 5개 만점에 ', '')
    temp = temp[0]
    stars_list.append(temp)
print(review_list)
print(stars_list)
print(len(review_list))
print(len(stars_list))

ba_comments = {}
ba_comments['text'] = review_list
ba_comments['score'] = stars_list

pd.DataFrame(ba_comments).to_csv('app_v2.csv')
driver.close()