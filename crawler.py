'''
我需要你幫我完成一下一些搜尋的小部分功能
因為我的搜尋有可能搜尋完不足4個資訊
如果搜尋完 在畫面上的 h2 id="searchModuleTitle" 裡面的內容為 No matches. 那應該直接結束 然後顯示沒有東西
如果少於四個資訊 你就應該動態的有多少個抓多少個。
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import parsing

driver_path = "chromedriver.exe"
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

ingredients = ['banana', 'breakfast']

driver.get('https://www.food.com/search/')

wait = WebDriverWait(driver, 2)

search_input = wait.until(EC.element_to_be_clickable((By.ID, 'search-input')))

ingredient = " and ".join(ingredients)

print(ingredient)
search_input.clear()
search_input.send_keys(ingredient)
search_input.send_keys(Keys.RETURN)

wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'inner-wrapper')))

links = driver.find_elements(By.CSS_SELECTOR, '.inner-wrapper a')

find = []
for link in links[:4]:
    href = link.get_attribute('href')
    find.append(href)

for link in find:
    print(link)
    print(parsing.parse_recipe(link))

driver.quit()
