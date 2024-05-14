from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 設定WebDriver（這裡以Chrome為例）
driver_path = 'C:/Users/cake1/OneDrive/桌面/ML_Final/chromedriver.exe'  # 替換為你的chromedriver路徑
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# 設定要搜索的食材列表
ingredients = ['banana', 'egg', 'breakfast', 'Fall']

# 打開食譜網站
driver.get('https://www.food.com/search/')

# 等待頁面加載
wait = WebDriverWait(driver, 10)  # 最長等待時間為10秒

# 查找搜索輸入框
search_input = wait.until(EC.element_to_be_clickable((By.ID, 'search-input')))

ingredient = " and ".join(ingredients)

print(ingredient)
search_input.clear()
search_input.send_keys(ingredient)
search_input.send_keys(Keys.RETURN)
time.sleep(5)

# 關閉瀏覽器
driver.quit()
