from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import json

driver_path = "chromedriver.exe"
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

url = "https://www.food.com/recipe/spinach-and-cheese-stuffed-chicken-breast-rsc-495271"
driver.get(url)

data = {}

head = driver.find_element(By.CLASS_NAME, "svelte-1muv3s8").text
data['HEAD'] = head

content = driver.find_element(By.CLASS_NAME, "text.svelte-1aswkii.truncated").text
data['content'] = content

pic_url = driver.find_element(By.CLASS_NAME, "primary-image.svelte-wgcq7z").find_element(By.TAG_NAME, "img").get_attribute('src')
data['pics'] = pic_url

ingredients = []
ingredients_elements = driver.find_elements(By.CSS_SELECTOR, "ul.ingredient-list.svelte-1dqq0pw li")
for element in ingredients_elements:
    quantity = element.find_element(By.CLASS_NAME, "ingredient-quantity.svelte-1dqq0pw").text
    text = element.find_element(By.CLASS_NAME, "ingredient-text.svelte-1dqq0pw").text
    ingredients.append(quantity + " " + text)
data['ingredients'] = ingredients

directions = []
ind = 1
directions_section = driver.find_element(By.CLASS_NAME, "directions.svelte-1dqq0pw")
directions_elements = directions_section.find_elements(By.CSS_SELECTOR, "ul.direction-list.svelte-1dqq0pw li")
for element in directions_elements:
    direction = str(ind) + '. ' + element.text
    directions.append(direction)
    ind += 1
data['directions'] = directions

nutrition_script = driver.find_element(By.XPATH, "//script[@type='application/ld+json']")
nutrition_data = json.loads(nutrition_script.get_attribute('innerHTML'))
nutrition_info = nutrition_data['nutrition']

nutrition = [
    "calories " + str(nutrition_info['calories']) + "g",
    "fatContent " + str(nutrition_info['fatContent']) + "g",
    "saturatedFatContent " + str(nutrition_info['saturatedFatContent']) + "g",
    "cholesterolContent " + str(nutrition_info['cholesterolContent']) + "mg",  # mg單位
    "sodiumContent " + str(nutrition_info['sodiumContent']) + "mg",  # mg單位
    "carbohydrateContent " + str(nutrition_info['carbohydrateContent']) + "g",
    "fiberContent " + str(nutrition_info['fiberContent']) + "g",
    "sugarContent " + str(nutrition_info['sugarContent']) + "g",
    "proteinContent " + str(nutrition_info['proteinContent']) + "g"
]
data['nutrition'] = nutrition

print(data)

driver.quit()
