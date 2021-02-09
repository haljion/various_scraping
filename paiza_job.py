import requests
import re
import pandas as pd
import mojimoji as mj
import chromedriver_binary
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup

url = "https://paiza.jp/sign_in"
email = "yuji.takahashi0613@gmail.com"
password = "haljion11"

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

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

cur_url = driver.current_url
pages = driver.find_elements_by_css_selector(".c-pager-text")[-2].text
data_list = []


for i in range(1, int(pages) + 1):
    if i > 1:
        driver.get(next_url)
        sleep(3)
    
    job_titles = [
        t.text for t in driver.find_elements_by_css_selector(".c-job_offer-box__header__title")
    ]
    require_ranks = [
        r.text[-1] for r in driver.find_elements_by_css_selector(".a-heading-primary-small")
        ]
    job_detail_link = [
        a.get_attribute("href") for a in driver.find_elements_by_css_selector(".c-job_offer-actions__button")
        ]
    

    for title, rank, link in zip(job_titles, require_ranks, job_detail_link):
        con_flg = False
        driver.get(link)
        sleep(3)

        if rank == "S":
            continue

        sleep(3)

        # 応募要件
        requirements = driver.find_element_by_id("job-offer-recruitement-requirements")
        must_r = requirements.find_elements_by_css_selector(".m-definitions__description")[0].text
        must_r = must_r.replace("以下すべてのご経験をお持ちの方からのご応募をおまちしています！\n", "")
        must_r_list = must_r.split("\n")


        for r in must_r_list:
            r = r.split("　")

            if "研究開発" in r[0] and "趣味" not in r[-1]:
                con_flg = True
                break

            lan_list = r[0].split(", ")

            if "," in r[0] and "Java" not in lan_list and "実務" in r[-1]:
                con_flg = True
                break

            r = mj.zen_to_han(r[-1])
            r = re.sub("\\D", "", r)
            
            if int(r) >= 3:
                con_flg = True
                break
        
        if con_flg:
            continue


        must_r = must_r.replace("　", " ")
        must_r = must_r.replace("、", ",")
        must_r = must_r.replace("（", "(")
        must_r = must_r.replace("）", ")")
        must_r = must_r.replace("何らかのシステム開発", "業界")

        # 企業名
        corpname = driver.find_element_by_id("corpname").text

        title = title.replace("\nnew", "")
        data_list.append([
            corpname, title, must_r, rank, link
            ])
        sleep(3)
    

    next_url = cur_url + "?page=" + str(i+1)
    sleep(3)

driver.quit()

df = pd.DataFrame(
    data_list,
    columns=[
        "corpname", 
        "title", 
        "requirement", 
        "rank", 
        "link"
        ]
)
df.to_csv("paiza_job.csv")
