# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# import time

# # === CONFIGURE THESE ===
# URL = "https://store.playstation.com/en-hk/pages/latest"

# # Use the full class name as a CSS selector
# # BUTTON_SELECTOR = (By.CSS_SELECTOR, ".psw-solid-link.psw-button.psw-b-0.psw-t-button.psw-l-line-center.psw-button-sizing.psw-button-sizing--medium.psw-tertiary-button.psw-solid-button")
# BUTTON_SELECTOR = (By.CSS_SELECTOR, "a[href='/en-hk/category/3bf499d7-7acf-4931-97dd-2667494ee2c9/1']")
# # =======================

# options = webdriver.ChromeOptions()
# options.add_argument('--start-maximized')
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# driver.get(URL)

# try:
#     # Wait for the button to be clickable
#     button = WebDriverWait(driver, 15).until(
#         EC.element_to_be_clickable(BUTTON_SELECTOR)
#     )
#     button.click()
#     print("Button clicked!")
#     time.sleep(5)  # Wait to observe the result
# finally:
#     driver.quit() 



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

URL = "https://store.playstation.com/en-hk/pages/latest"
BUTTON_SELECTOR = ".psw-solid-link.psw-button.psw-b-0.psw-t-button.psw-l-line-center.psw-button-sizing.psw-button-sizing--medium.psw-tertiary-button.psw-solid-button"

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(URL)

try:
    # Wait for at least two buttons to be present
    WebDriverWait(driver, 15).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, BUTTON_SELECTOR)) >= 2
    )
    buttons = driver.find_elements(By.CSS_SELECTOR, BUTTON_SELECTOR)
    second_button = buttons[1]  # Index 1 is the second button
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(@class, 'psw-solid-link') and contains(@class, 'psw-button') and contains(@class, 'psw-tertiary-button')])[2]")))
    second_button.click()
    print("Second button clicked!")
    time.sleep(5)
finally:
    driver.quit()
