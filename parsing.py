from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import json

def parse_recipe(url):
    driver_path = "chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    
    try:
        json_element = driver.find_element(By.XPATH, "//script[@type='application/ld+json']")
        recipe_json = json.loads(json_element.get_attribute('innerHTML'))
        
        data = {
            'text': recipe_json['name'],
            'description': recipe_json['description'],
            'img': recipe_json['image'],
            'ingredients': [ingredient for ingredient in recipe_json['recipeIngredient']],
            'directions': [step['text'] for step in recipe_json['recipeInstructions']],
            'nutrition': [
                f"calories {recipe_json['nutrition']['calories']}g",
                f"fatContent {recipe_json['nutrition']['fatContent']}g",
                f"saturatedFatContent {recipe_json['nutrition']['saturatedFatContent']}g",
                f"cholesterolContent {recipe_json['nutrition']['cholesterolContent']}mg",
                f"sodiumContent {recipe_json['nutrition']['sodiumContent']}mg",
                f"carbohydrateContent {recipe_json['nutrition']['carbohydrateContent']}g",
                f"fiberContent {recipe_json['nutrition']['fiberContent']}g",
                f"sugarContent {recipe_json['nutrition']['sugarContent']}g",
                f"proteinContent {recipe_json['nutrition']['proteinContent']}g"
            ]
        }
    finally:
        driver.quit()
    
    return data
