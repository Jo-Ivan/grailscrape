# grailscrape

## Before using
This project is solely for analyzing data and not for commercial use.

**Data scraping is against** [**Grailed's Terms of Service**](https://www.grailed.com/about/terms).

Please use at your own discretion.

## Running locally
Make sure you have these installed:
- [ChromeDriver](https://chromedriver.chromium.org/)
- [Python](https://www.python.org/downloads/)
- [Selenium with Python](https://selenium-python.readthedocs.io/installation.html)
- [pandas](https://pandas.pydata.org/docs/getting_started/index.html#getting-started)
  
In grailscrape.py file:
```
# Change PATH depending on where you have ChromeDriver installed
driver = webdriver.Chrome('./chromedriver')
```
## How to use
```
python3 grailscrape.py 'undercover jacket'
```

### Todos
- [ ] extract link of listing
- [ ] extract image links 
- [ ] data analysis
- [ ] find a way to remove fail-safes
- [x] automatic searching
- [x] export csv
- [x] fix dates (seperate last bumped and listing created)
- [x] close create account modal when it pops up
- [x] fix bug when scrolling to end of page

### Feel free to contribute!
