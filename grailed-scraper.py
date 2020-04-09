from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

import pandas as pd
import argparse
import time


url = 'https://www.grailed.com/'
driver = webdriver.Chrome('./chromedriver')

parser = argparse.ArgumentParser()
parser.add_argument("search", help="Query to find listings on Grailed.com")
args = parser.parse_args()

search_term = args.search


def load_grailed_url():
    driver.get(url)

    input_box = driver.find_element_by_id("globalheader_search")
    input_box.send_keys(search_term)
    input_box.send_keys(Keys.RETURN)

    # Error if search bar not found after 10 seconds
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "shop"))
        )
    except TimeoutException:
        print("Loading took too much time!")

    # Wait for feed-items to appear
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "listing-cover-photo"))
        )
    except TimeoutException:
        print("No listings showed up after 10 seconds!")


def close_modal():
    driver.implicitly_wait(5)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()


def scroll_to_end():
    SCROLL_PAUSE_TIME = 10.0

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def extract_post_information():
    all_posts = driver.find_elements_by_class_name('feed-item')

    item_brands = []
    item_names = []
    item_sizes = []
    current_prices = []
    old_prices = []
    created_at_dates = []
    last_bumped_dates = []
    is_staff_pick = []
    is_by_grailed = []

    for post in all_posts:
        item = post.text.split('$')

        if len(item) == 3:
            new_price = item[1]
            old_price = item[2]
            current_price = new_price
        else:
            regular_price = item[1]
            old_price = 'n/a'
            current_price = regular_price

        item = item[0].split('\n')

        if item[0] == 'Staff Pick':
            item_brand = item[2]
            item_name = item[4]
            item_size = item[3]
            date = item[1]
            staff_pick = True
            by_grailed = False
        elif item[0] == 'By Grailed':
            item_brand = item[2]
            item_name = item[4]
            item_size = item[3]
            date = item[1]
            staff_pick = False
            by_grailed = True
        else:
            item_brand = item[1]
            item_name = item[3]
            item_size = item[2]
            date = item[0]
            staff_pick = False
            by_grailed = False

        dates = date.split('(')

        if len(dates) == 2:
            last_bumped = dates[0]
            created_at = dates[1]
            created_at = created_at[:-1]
        else:
            last_bumped = 'n/a'
            created_at = dates[0]

        item_brands.append(item_brand)
        item_names.append(item_name)
        item_sizes.append(item_size)
        last_bumped_dates.append(last_bumped)
        created_at_dates.append(created_at)
        is_staff_pick.append(staff_pick)
        is_by_grailed.append(by_grailed)
        old_prices.append(old_price)
        current_prices.append(current_price)

        # print(
        #     f'brand: {item_brand}, name: {item_name}, size: {item_size}, date: {date}, staff pick?: {staff_pick}, current price: {current_price}, old price: {old_price}')

    listing = {'brand': item_brands, 'name': item_names, 'size': item_sizes, 'created_at': created_at_dates, 'last_bumped_date': last_bumped_dates,
               'old price': old_prices, 'current price': current_prices, 'by grailed': is_by_grailed, 'staff pick': is_staff_pick}
    df = pd.DataFrame(listing)

    df.to_csv('listings.csv')


# def extract_image_url():
#     image_urls = []
#     count = 0

#     listings = driver.find_elements_by_class_name("feed-item")
#     listings.reverse()
#     for listing in listings:
#         if len(listing.find_elements_by_class_name("lazyload-placeholder")) == 0:
#             image_url = listing.find_element_by_tag_name(
#                 "img").get_attribute("src")
#             image_urls.append(image_url)


start = pd.Timestamp.now()
print(f'You searched for {search_term}')

load_grailed_url()
time.sleep(7)
scroll_to_end()

listing_count = driver.find_element_by_xpath(
    "//*[@id='shop']/div/div/div[1]/div[1]/div")

print(f'Scraping {listing_count.text} please wait 🐶')
print('...')

close_modal()
time.sleep(5)
scroll_to_end()

print('Extracting data.')
extract_post_information()

print(f'All done! ⚡️')

print(pd.Timestamp.now()-start)
# extract_image_url()

driver.close()
