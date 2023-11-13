from selenium import webdriver
from scrapy import Selector
import time
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
website_url = input("Enter domain url: ")
#driver.get('https://www.hackerrank.com/domains/python')
driver.get(website_url)
login_button = driver.find_element(By.CSS_SELECTOR, 'button.hrds-btn.login-btn')
login_button.click()
time.sleep(5)

username_input = driver.find_element(By.XPATH, "//input[@placeholder='Your username or email']")
username = input("Enter Username: ")
username_input.send_keys(username)

password_input = driver.find_element(By.XPATH, "//input[@placeholder='Your password']")
password = input("Enter your password: ")
password_input.send_keys(password)

submit_button = driver.find_element(By.XPATH, "//button[@data-analytics='LoginPassword']")
submit_button.click()
time.sleep(3)

last_height = driver.execute_script("return document.body.scrollHeight")
while True:
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
  time.sleep(5)
  new_height = driver.execute_script("return document.body.scrollHeight")
  if new_height == last_height:
    break
  last_height = new_height
selenium_response_text = driver.page_source
response = Selector(text=selenium_response_text)
a_elements = response.xpath('//a[contains(@class, "js-track-click challenge-list-item")]')
questions = response.xpath("//h4[@class='challengecard-title']")
urls = []
for idx,a_element in enumerate(a_elements):
  url = a_element.xpath('@href').get()
  h4_text = a_element.xpath('.//h4[contains(@class, "challengecard-title")]/text()').get()
  if url and h4_text:
    urls.append({'name':h4_text,'url':'https://www.hackerrank.com/'+url})
    # f = open("output.py", "w")
    # f.write(f"{idx+1}. {h4_text.strip()} \n")
for i,element in enumerate(urls, 1):
  time.sleep(3)
  driver.get(element['url'])
  # icon_element = driver.find_element(By.CSS_SELECTOR, 'i.ui-icon-cross.close-icon')
  # if icon_element:
    # icon_element.click()
    # time.sleep(3)
  page_source = driver.page_source
  sel = Selector(text=page_source)
  # problem_statement = sel.xpath('//div[@class="challenge_problem_statement"]//p')
  paragraphs = driver.find_elements(By.CSS_SELECTOR, "div.hackdown-content p, div.hackdown-content div.highlight")
  f = open(f"{i}.{element['name']}.py", "w")
  f.write('\'\'\'\n')
  for paragraph in paragraphs:
    text = paragraph.text
    f.write(f'{text}\n')
  time.sleep(3)
  f.write(f'\'\'\'')
f.close()
driver.close()
