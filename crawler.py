from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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

print(find)
driver.quit()
