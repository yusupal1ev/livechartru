import os
import json

from decimal import Decimal
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from django.conf import settings


def crawler(season, year, form):
    if not settings.DEBUG:
        html = get_html_through_selenium(season, year, form)
        create_html_backup(season, year, form, html)

    else:
        html = get_html_from_backup(season, year, form)

    soup = BeautifulSoup(html, 'lxml')
    seasons = get_seasons(soup)
    titles = []
    for article in soup('article', class_='anime'):
        data_id = int(article['data-anime-id'])
        title_english = article['data-english']
        title_native = article['data-native']
        title_romaji = article['data-romaji']
        premiere = int(article['data-premiere'])
        premiere_precision = int(article['data-premiere-precision'])

        try:
            categories = [i.find('a').string.strip() for i in article.find('ol', class_='anime-tags')('li')]
        except AttributeError:
            categories = []

        try:
            studios = [i.find('a').string.strip() for i in article.find('ul', class_='anime-studios')('li')]
        except AttributeError:
            studios = [i.string.strip() for i in article.find('ul', class_='anime-studios')('li')]

        try:
            rating = Decimal(article.find('div', class_='anime-extras').find('div', class_='anime-avg-user-rating').text.strip())
        except AttributeError:
            rating = None

        date = article.find('div', class_='anime-date').text.strip()
        source = article.find('div', class_='anime-metadata').find('div', class_='anime-source').text.strip()
        series = article.find('div', class_='anime-metadata').find('div', class_='anime-episodes').text.strip().split("×")

        try:
            episodes = int(series[0].strip().split(' ')[0])
        except ValueError:
            episodes = None

        try:
            duration = int(series[1].strip().split(' ')[0])
        except (ValueError, IndexError):
            duration = None

        paragraphs = [p.text.strip() for p in
                      article.find('div', class_='anime-info').find('div', class_='anime-synopsis').find_all('p') if
                      'Source:' not in p.text.strip()]
        description = '\n'.join(paragraphs)
        classes = article.find('div', class_='anime-info').find('div', class_='anime-synopsis').attrs['class']
        if 'is-spoiler-masked' in classes:
            spoiler = True
        else:
            spoiler = False

        image_url = article.find('img', class_='lazy-img')['data-srcset'].split(' ')[-2]

        titles.append({"data_id": data_id,
                       "title_english": title_english,
                       "title_native": title_native,
                       "title_romaji": title_romaji,
                       "premiere": premiere,
                       "premiere_precision": premiere_precision,
                       "categories": categories,
                       "rating": rating,
                       "studios": studios,
                       "date": date,
                       "source": source,
                       "episodes": episodes,
                       "duration": duration,
                       "description": description,
                       "spoiler": spoiler,
                       "image_url": image_url,
                       "season": season,
                       "year": year,
                       "form": form,
                       }
                      )
    return titles, seasons


def get_html_through_selenium(season, year, form):
    url = f"https://www.livechart.me/{season}-{year}/{form}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    with open(os.path.join(settings.BASE_DIR, "cookies.json")) as f:
        cookies = json.load(f)
        print(cookies[0])

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    # options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.add_cookie(cookies[0])
    driver.get(url)
    sleep(3)
    # cookies = driver.get_cookies()
    # with open("cookies.json", "w") as f:
    #     json.dump(cookies, f)

    html = driver.page_source
    driver.quit()
    return html


def create_html_backup(season, year, form, html):
    with open(os.path.join(settings.BASE_DIR, f'backend/backups/{season}-{year}-{form}.html'), 'w') as f:
        f.write(html)


def get_html_from_backup(season, year, form):
    with open(os.path.join(settings.BASE_DIR, f'backend/backups/{season}-{year}-{form}.html'), 'r') as f:
        html = f.read()
        return html


def get_seasons(soup: BeautifulSoup):
    months = {"spring": 4, "summer": 7, "fall": 10, "winter": 1}
    seasons = []
    cells = soup.find('li', class_='has-browse-menu').find('div', class_='small-up-4').find_all('div', class_='cell')
    for cell in cells:
        cell: BeautifulSoup
        text = cell.find('a').text.strip()
        if text != 'More':
            season = text.split(' ')[0].lower()
            seasons.append({
                "season": season,
                "year": int(text.split(' ')[1]),
                "month_started": months[season],
                "month_ended": months[season] + 2,
            })

    return seasons
