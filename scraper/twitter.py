from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
from credentials import TWITTER_USERNAME, TWITTER_PASSWORD

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
LOGIN = "https://twitter.com/i/flow/login"

login_page = driver.get(LOGIN)
sleep(3)

login_input = driver.find_element(By.TAG_NAME, "input")
print(TWITTER_USERNAME)
login_input.send_keys(TWITTER_USERNAME)
login_input.send_keys(Keys.ENTER)
sleep(3)

password_input = driver.find_element(By.NAME, "password")
password_input.send_keys(TWITTER_PASSWORD)
password_input.send_keys(Keys.ENTER)