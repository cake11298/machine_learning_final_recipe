from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 初始化 WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 您要抓取的食譜網址
url = "https://www.food.com/recipe/bourbon-chicken-45809"
driver.get(url)

# 創建一個空字典來儲存抓取的資料
data = {}

# 抓取 Head
head = driver.find_element(By.CLASS_NAME, "svelte-1muv3s8").text
data['HEAD'] = head

# 抓取 Content
content = driver.find_element(By.CLASS_NAME, "text.svelte-1aswkii.truncated").text
data['content'] = content

# 抓取圖片網址
pic_url = driver.find_element(By.CLASS_NAME, "primary-image.svelte-wgcq7z").find_element(By.TAG_NAME, "img").get_attribute('src')
data['pics'] = pic_url

# 抓取所有成分，包括數量和描述
ingredients = []
ingredients_elements = driver.find_elements(By.CSS_SELECTOR, "ul.ingredient-list.svelte-1dqq0pw li")
for element in ingredients_elements:
    quantity = element.find_element(By.CLASS_NAME, "ingredient-quantity.svelte-1dqq0pw").text
    text = element.find_element(By.CLASS_NAME, "ingredient-text.svelte-1dqq0pw").text
    ingredients.append(quantity + " " + text)  # 數量和成分描述合併成一個字符串
data['ingredient'] = ingredients

# 打印出抓取的資料
print(data)

# 關閉瀏覽器
driver.quit()
