from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
from bs4 import BeautifulSoup

# List of realistic user agents to rotate
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
]

# Select a random user agent
random_user_agent = random.choice(USER_AGENTS)

chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# Add the randomly selected user agent
chrome_options.add_argument(f"--user-agent={random_user_agent}")
chrome_options.add_argument("--accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
chrome_options.add_argument("--accept-language=en-US,en;q=0.5")
chrome_options.add_argument("--window-size=1920,1080")  # Add window size
chrome_options.add_argument("--start-maximized")  # Start maximized

print(f"Using User-Agent: {random_user_agent}")

driver = webdriver.Chrome(options=chrome_options)

driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

url = "https://pk.indeed.com/"

try:
    time.sleep(10)
    driver.get(url)
    time.sleep(1000)
    
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    
    time.sleep(5)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    print(soup.prettify()[:2000])
    
    title = soup.find("title")
    if title:
        print(f"\nPage Title: {title.get_text()}")

except Exception as e:
    print(f"An error occurred: {e}")
    # Take screenshot for debugging
    driver.save_screenshot("error_screenshot.png")

finally:
    driver.quit()