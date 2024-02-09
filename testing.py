from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Set Chrome options for running in headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Runs Chrome in headless mode
chrome_options.add_argument('--no-sandbox') # Bypass OS security model
chrome_options.add_argument('--disable-gpu')  # applicable to windows os only
chrome_options.add_argument('--disable-dev-shm-usage')  # overcome limited resource problems
chrome_options.add_argument("--disable-extensions")

# Initialize the Chrome webdriver with headless mode
driver = webdriver.Chrome(options=chrome_options)

# Navigate to Google
driver.get("https://www.google.com")

# Find the search box and input a query
search_box = driver.find_element_by_name("q")
search_box.send_keys("OpenAI")
search_box.submit()

# Print the titles of the search results
search_results = driver.find_elements_by_css_selector("h3")
for result in search_results:
    print(result.text)

# Close the webdriver
driver.quit()
