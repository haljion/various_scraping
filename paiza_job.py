import requests
import chromedriver_binary
from time import sleep
from selenium import webdriver
# from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

url = "https://paiza.jp/sign_in"
email = "yuji.takahashi0613@gmail.com"
password = "haljion11"

driver = webdriver.Chrome()
driver.get(url)
sleep(3)

email_box = driver.find_element_by_id("email")
pass_box = driver.find_element_by_id("password")
email_box.send_keys(email)
pass_box.send_keys(password)
driver.find_elements_by_class_name("a-button-primary-large")[0].submit()
sleep(3)

driver.find_elements_by_link_text("エンジニア求人")[0].click()
sleep(3)

driver.find_elements_by_link_text("Python3")[-1].click()
sleep(3)

job_titles = driver.find_elements_by_css_selector(".c-job_offer-box__header__title")
job_detail_buttons = driver.find_elements_by_css_selector(".c-job_offer-actions__button")
pages = driver.find_elements_by_css_selector(".c-pager-text")[-2]
# url/page=15


for job_info in driver.find_elements_by_css_selector(".c-job_offer-box__header__title"):
    print(job_info.text)
    # ランク未達が含まれてたらスルー
    # job_info.c-job_offer-actions__button


# c-job_offer-box  c-job_offer-box--career


sleep(5)
driver.quit()