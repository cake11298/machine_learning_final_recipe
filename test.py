import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json

def parse_recipe(url, driver):
    try:
        driver.get(url)
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
    except Exception as e:
        print(f"Error processing URL {url}: {str(e)}")
        return {}
    finally:
        driver.quit()  # Ensure each thread cleans up its WebDriver instance
    return data

def thread_function(url, results):
    driver_path = "chromedriver.exe"
    service = Service(driver_path)
    options = Options()
    options.add_argument("--headless")  # Ensure operation in headless mode
    options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")  # Use a common user-agent
    driver = webdriver.Chrome(service=service, options=options)
    results.append(parse_recipe(url, driver))

def crawler():
    driver_path = "chromedriver.exe"
    service = Service(driver_path)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")  # Use a common user-agent
    driver = webdriver.Chrome(service=service, options=options)

    ingredients = ['lemon']
    driver.get('https://www.food.com/search/')
    wait = WebDriverWait(driver, 10)  # Increased timeout for reliability

    search_input = wait.until(EC.element_to_be_clickable((By.ID, 'search-input')))
    ingredient = " and ".join(ingredients)
    search_input.clear()
    search_input.send_keys(ingredient)
    search_input.send_keys(Keys.RETURN)

    try:
        wait.until(EC.visibility_of_element_located((By.ID, 'searchModuleTitle')))
        no_match_text = driver.find_element(By.ID, 'searchModuleTitle').text
        if "No matches" in no_match_text:
            print("No matches found.")
            return []
        
        links = driver.find_elements(By.CSS_SELECTOR, '.inner-wrapper a')
        links = [link.get_attribute('href') for link in links[:3]]  # Fetch up to the first four links or fewer if less are found
    finally:
        driver.quit()  # Quit the initial search driver after fetching links

    results = []
    threads = []

    # Create a thread for each URL to be processed
    for url in links:
        thread = threading.Thread(target=thread_function, args=(url, results))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete their tasks
    for thread in threads:
        thread.join()

    return results
