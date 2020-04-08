from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

url = 'https://www.grailed.com/shop/4rtigaaOuw'
driver = webdriver.Chrome('./chromedriver')

# delay = 10

# num_page_items = len(driver.find_elements_by_class_name('original-price'))

# title = []
# price = []


# all_titles = driver.find_elements_by_class_name('listing-title')
# all_prices = driver.find_elements_by_class_name('original-price')


# for i in range(num_page_items):
#     title.append(all_titles[i].text)
#     price.append(all_prices[i].text)

# for i in range(num_page_items):
#     print(title[i] + ': ' + price[i])


def load_grailed_url():
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "shop"))
        )
    except TimeoutException:
        print("Loading took too much time!")


def extract_post_information():
    all_posts = driver.find_elements_by_class_name('feed-item')
    post_title_list = []
    for post in all_posts:
        print(post.text)
        post_title_list.append(post.text)


load_grailed_url()
extract_post_information()


driver.close()
