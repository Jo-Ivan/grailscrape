import time
from selenium import webdriver

driver = webdriver.Chrome('./chromedriver')
driver.get('https://www.grailed.com/shop/4rtigaaOuw')

time.sleep(10)

num_page_items = len(driver.find_elements_by_class_name('original-price'))

name = driver.find_elements_by_class_name('listing-title')
price = driver.find_elements_by_class_name('original-price')

for i in range(num_page_items):
    print(name[i].text)
    print(price[i].text)
