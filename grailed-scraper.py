from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

url = 'https://www.grailed.com/shop/4rtigaaOuw'
driver = webdriver.Chrome('./chromedriver')

delay = 10


def load_grailed_url():
    driver.get(url)
    try:
        WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.ID, "shop"))
        )
    except TimeoutException:
        print("Loading took too much time!")

    try:
        WebDriverWait(driver, delay).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "listing-cover-photo"))
        )
    except TimeoutException:
        print("No listings showed up after 10 seconds!")


def extract_post_information():
    all_posts = driver.find_elements_by_class_name('feed-item')

    item_brands = []
    item_names = []
    item_sizes = []
    current_prices = []
    dates = []
    is_staff_pick = []

    for post in all_posts:
        item = post.text.split('$')

        if len(item) == 3:
            slashed_price = item[1]
            old_price = item[2]
            current_prices.append(slashed_price)
        else:
            regular_price = item[1]
            current_prices.append(regular_price)

        item = item[0].split('\n')

        if item[0] == 'Staff Pick':
            item_brand = item[2]
            item_name = item[4]
            item_size = item[3]
            date = item[1]
            staff_pick = True
        else:
            item_brand = item[1]
            item_name = item[3]
            item_size = item[2]
            date = item[0]
            staff_pick = False

        item_brands.append(item_brand)
        item_names.append(item_name)
        item_sizes.append(item_size)
        dates.append(date)
        is_staff_pick.append(staff_pick)

        print(
            f'brand: {item_brand}, name: {item_name}, size: {item_size}, date: {date}, staff pick?: {staff_pick}')


load_grailed_url()
extract_post_information()


driver.close()
