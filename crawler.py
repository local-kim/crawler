import os, sys
from urllib.request import urlopen
from selenium import webdriver
import mysql.connector as mariadb

# connect to database
conn = mariadb.connect(
    user="root",
    password="1234",
    host="localhost",
    database="project")
cur = conn.cursor()

driver = webdriver.Chrome()
base_url = 'https://www.animal.go.kr/front/awtis/loss/lossList.do?totalCount=118&pageSize=10&menuNo=1000000057&&page='
path = '/Users/hyunji/project/crawler/img/'
page_end = 10
page_size = 10

for page in range(1, page_end + 1):
    for n in range(1, page_size + 1):   # click
        driver.get(base_url + str(page))
        driver.find_element_by_css_selector('ul.list > li:nth-child(' + str(n) + ') > div.photo > a').click()

        img_url = driver.find_element_by_css_selector('div > div.photo > a > img').get_attribute('src')
        value = driver.find_element_by_css_selector('input#seqNo').get_attribute('value')
        location = driver.find_element_by_css_selector('div > table > tbody > tr:nth-child(8) > td').text
        date = driver.find_element_by_css_selector('div > table > tbody > tr:nth-child(6) > td').text
        page_url = driver.current_url

        file_name = 'lost_' + value +'.jpg'

        # print(file_name)
        # print(page_url)
        # print(location)
        # print(date)

        # check if file already exists
        if os.path.exists(path + file_name):
            driver.quit()
            conn.commit()
            conn.close()
            sys.exit(1)

        # insert data to DB
        try:
            cur.execute("INSERT INTO losts VALUES (%s, %s, %s, %s)", (file_name, page_url, location, date))
        except mariadb.Error as e:
            print(f"Error: {e}")

        # download images
        with urlopen(img_url) as f:
            with open(path + file_name,'wb') as h:
                img = f.read()
                h.write(img)

print('Download complete')

driver.quit()
conn.commit()
conn.close()