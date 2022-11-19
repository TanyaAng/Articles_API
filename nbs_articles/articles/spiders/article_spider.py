import json
import scrapy
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from jsonschema import validate
from sqlalchemy.orm import Session

from articles import items
from dao import repository
from dao.repository import check_article_existence
from models.dto.article_dto import ArticleCreateDTO
from models.dto.label_dto import LabelCreateDTO
from models.dto.link_dto import LinkCreateDTO
from util import database_connector
from util.database_connector import engine, SessionLocal

database_connector.Base.metadata.create_all(bind=engine)

db = SessionLocal()


def create_article(item: items.ArticlesItem, db: Session = db):
    with open('items.json', 'a') as file:
        json.dump({
            'date': item['date'],
            'url': item['url'],
            'labels': item['labels'],
            'links': item['links'],
            'body': item['body'],
        }, file)

    article_dto = ArticleCreateDTO(
        date=item['date'],
        url=item['url'],
        body=item['body']
    )

    label_dtos = []
    for label in item['labels']:
        label_dtos.append(LabelCreateDTO(label=label))

    link_dtos = []
    for link in item['links']:
        if link is not None:
            link_dtos.append((LinkCreateDTO(link=link)))

    return repository.create_article(
        article_dto=article_dto,
        labels=label_dtos,
        links=link_dtos,
        db=db
    )


schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    'type': 'object',
    'properties': {
        'date': {'type': 'string'},
        'url': {'type': 'string'},
        'labels': {'type': 'array', 'items': [{'type': 'string'}]},
        'links': {'type': 'array', 'items': [{'type': 'string'}]},
        'body': {'type': 'string'},
    },
    'required': ['date', 'url', 'labels', 'body']
}


class ArticleSpider(scrapy.Spider):
    name = 'article'
    start_urls = [
        'https://nbs.sk/en/press/news-overview/',
    ]

    def start_requests(self):

        for page in range(0, 31, 5):
            url = self.start_urls[
                      0] + f'/?table_post-list_params=%7B"offset"%3A{page}%2C"filter"%3A%7B"lang"%3A"en"%7D%7D'
            yield scrapy.Request(url, callback=self.parse_page, )

    def parse_page(self, response, **kwargs):
        driver = webdriver.Chrome('D:\ChromeDriver\chromedriver.exe')
        url = response.url
        driver.get(url)
        archive_results = driver.find_elements(By.CLASS_NAME, 'archive-results__item')
        for page in archive_results:
            url = page.get_attribute('href')
            yield scrapy.Request(url, callback=self.parse_article)
        driver.quit()

    def parse_article(self, response, **kwargs):
        driver = webdriver.Chrome('D:\ChromeDriver\chromedriver.exe')
        url = response.url
        driver.get(url)
        try:
            date = driver.find_element(By.CSS_SELECTOR, '.nbs-post .nbs-post__date')
            links = driver.find_elements(By.CSS_SELECTOR, '.nbs-post a')
            labels = driver.find_elements(By.CSS_SELECTOR, '.nbs-post .label--sm')
            body = driver.find_element(By.CSS_SELECTOR, '.nbs-post .nbs-post__block')

            label_data = {
                'date': date.text,
                'url': url,
                'labels': [label.text for label in labels],
                'links': [link.get_attribute('href') for link in links],
                'body': body.text,
            }

            validate(instance=label_data, schema=schema)

            item = items.ArticlesItem()
            item['date'] = label_data['date']
            item['url'] = label_data['url']
            item['body'] = label_data['body']
            item['labels'] = label_data['labels']
            item['links'] = label_data['links']

            if check_article_existence(db, item['url']):
                create_article(item, db)
        except Exception:
            pass

        driver.quit()

# Terminal: scrapy crawl article
# scrapy crawl article -o items.json
