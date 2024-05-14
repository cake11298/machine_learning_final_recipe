from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver_path = 'chromedriver.exe'
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

ingredients = ['banana', 'egg', 'breakfast', 'Fall']

driver.get('https://www.food.com/search/')

wait = WebDriverWait(driver, 10)

search_input = wait.until(EC.element_to_be_clickable((By.ID, 'search-input')))

ingredient = " and ".join(ingredients)

print(ingredient)
search_input.clear()
search_input.send_keys(ingredient)
search_input.send_keys(Keys.RETURN)
time.sleep(5)

driver.quit()
