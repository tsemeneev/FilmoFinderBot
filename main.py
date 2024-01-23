import re
import time
from pprint import pprint

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def get_seasons(series, seasons):
    if len(seasons) > 1:

        for season in seasons:
            if season.find_element(By.TAG_NAME, 'a').text == 'Без категории':
                continue

            season_link = season.find_element(By.TAG_NAME, 'a').get_attribute('href')
            season_title = season.find_element(By.TAG_NAME, 'a').text
            season_page = requests.get(season_link)
            soup = BeautifulSoup(season_page.text, 'html.parser')
           
            url = soup.find('a', {'itemprop': 'url'}).get('href')
            fist_episode = requests.get('https://hlamer.ru/' + url)
            soup = BeautifulSoup(fist_episode.text, 'html.parser')
            url = soup.find('link', {'itemprop': 'embedUrl'}).get('href')

            series['seasons'].append({
                'title': season_title,
                'url': url
            })

        return series
    else:
        season_link = seasons[0].find_element(By.TAG_NAME, 'a').get_attribute('href')
        season_title = seasons[0].find_element(By.TAG_NAME, 'a').text
        season_page = requests.get(season_link)

        soup = BeautifulSoup(season_page.text, 'html.parser')
        url = soup.find('a', {'itemprop': 'url'}).get('href')
        fist_episode = requests.get('https://hlamer.ru/' + url)
        soup = BeautifulSoup(fist_episode.text, 'html.parser')
        url = soup.find('link', {'itemprop': 'embedUrl'}).get('href')
        series['seasons'].append({
            'title': season_title,
            'url': url
        })

    return series


def is_film(driver, poster):
    driver.find_element(By.CLASS_NAME, 'video-gallery').find_element(By.TAG_NAME, 'a').click()
    time.sleep(1)
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    title = soup.find('h1').text

    description = soup.find('div', {'class': 'breakword-250'}).text
    url = soup.find('link', {'itemprop': 'embedUrl'}).get('href')
    film = {
        'title': title,
        'description': description[0:400] + '...',
        'poster': poster,
        'url': url
    }

    return film


def is_series(driver, poster):
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    title = soup.find('h1').text
    description = soup.find('div', {'class': 'breakword-250'}).text

    series_dict = {
        'title': title,
        'description': description[0:400] + '...',
        'poster': poster,
        'seasons': []
    }
    seasons = driver.find_element(By.ID, 'channel-category-line').find_elements(By.TAG_NAME, 'li')[1:]

    try:

        if len(seasons) > 2 and 'https://hlamer.ru/' in seasons[2].find_element(By.TAG_NAME,
                                                                             'a').get_attribute(
            'href'):
            # если много сезонов, и они скрыты
            seasons[2].click()

        hidden_seasons = driver.find_element(By.ID, 'channel-category-line').find_elements(
            By.TAG_NAME, 'li')[1:]

        series = get_seasons(series_dict, hidden_seasons)
        return series

    except NoSuchElementException:  # если 1 или 2 сезона
        series = get_seasons(series_dict, seasons)
        return series


class Parser:
    def __init__(self):
        self.options = webdriver.ChromeOptions()

    def parse(self, film_name):
        # self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--window-size=1920,1080')
        self.options.add_argument('--disable-notifications')
        self.options.add_argument('--disable-infobars')
        self.options.add_argument('--disable-popup-blocking')
        self.options.add_argument('--disable-translate')

        driver = webdriver.Chrome(options=self.options)

        try:
            driver.get('https://hlamer.ru/')
            search_input = driver.find_element(By.ID, 'search')
            search_input.send_keys(film_name)
            search_input.send_keys(Keys.ENTER)
            time.sleep(1)
            films = driver.find_element(By.ID, 'block-main-content').find_elements(By.TAG_NAME, 'li')

            films[0].find_element(By.TAG_NAME, 'a').click()
            poster = driver.find_element(By.ID, 'photo-container').find_element(
                By.TAG_NAME, 'a').get_attribute('href')

            try:  # Если это сериал
                series = is_series(driver, poster)
                return series

            except NoSuchElementException:  # Если это фильм
                film = is_film(driver, poster)
                return film

        except Exception as e:
            return None

        finally:
            driver.close()
            driver.quit()


parser = Parser()

