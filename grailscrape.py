from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

import pandas as pd
import argparse
import time

url = 'https://www.grailed.com/'

# Change PATH depending on where you have ChromeDriver installed
driver = webdriver.Chrome('./chromedriver')

parser = argparse.ArgumentParser()
parser.add_argument("search", help="enter search argument")
args = parser.parse_args()

search_term = args.search


def load_grailed_url():
    driver.get(url)

    input_box = driver.find_element_by_id("globalheader_search")
    input_box.send_keys(search_term)
    input_box.send_keys(Keys.RETURN)

    # Wait for search bar to appear
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
    # Wait for modal to pop out
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "-content"))
        )
    except TimeoutException:
        print("Modal wasn't shown")

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "-title"))
        )
    except TimeoutException:
        print("Modal wasn't shown")

    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()


def check_listing_count():
    listing_count = driver.find_element_by_xpath(
        "//*[@id='shop']/div/div/div[1]/div[1]/div")

    if not listing_count.text:
        print('Scraping please wait 🐶')
    else:
        print(f'Scraping {listing_count.text} please wait 🐶')


def scroll_to_end():
    lenOfPage = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match = False
    while(match == False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount == lenOfPage:
            match = True


def extract_href_link():
    href_links = []
    all_posts = driver.find_elements_by_class_name(
        'feed-item')

    for link in all_posts:
        hrefs = link.find_elements_by_tag_name('a')
        for href in hrefs:
            href_links.append(href.get_attribute("href"))
    return href_links


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

    # Extracts all href links
    href_links = extract_href_link()

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

    listing = {'brand': item_brands, 'name': item_names, 'size': item_sizes, 'created_at': created_at_dates, 'last_bumped_date': last_bumped_dates,
               'old price': old_prices, 'current price': current_prices, 'by grailed': is_by_grailed, 'staff pick': is_staff_pick, 'link': href_links}
    df = pd.DataFrame(listing)

    df.to_csv('listings.csv')


start = pd.Timestamp.now()

print(f'You searched for {search_term}')

load_grailed_url()
time.sleep(10)
close_modal()
time.sleep(3)
check_listing_count()

print('Currently scrolling to end of page.')

# Scrolling fail-safes
scroll_to_end()
time.sleep(6)
scroll_to_end()
time.sleep(3)
scroll_to_end()

print('Extracting data, could take a while...')

extract_post_information()

print('All done! ⚡️')

print(pd.Timestamp.now()-start)

driver.close()
