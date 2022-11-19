import scrapy
from selenium import webdriver
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
from util.validators import date_convert, check_valid_link

database_connector.Base.metadata.create_all(bind=engine)

db = SessionLocal()


class ArticleSpider(scrapy.Spider):
    name = 'article'
    start_urls = [
        'https://nbs.sk/en/press/news-overview/',
    ]

    CHROME_DRIVER_PATH = 'D:\ChromeDriver\chromedriver.exe'
    PAGE_ARTICLES_CLASS_NAME = 'archive-results__item'
    ARTICLE_DATE_CSS_SELECTOR = '.nbs-post .nbs-post__date'
    LINK_CSS_SELECTOR = '.nbs-post a'
    LABEL_CSS_SELECTOR = '.nbs-post .label--sm'
    BODY_CSS_SELECTOR = '.nbs-post .nbs-post__block'
    MIN_PAGE_NUMBER = 0
    PAGE_STEP_PAGINATION = 5
    ARTICLES_MIN_NUMBER = 20

    def start_requests(self):
        for page in range(self.MIN_PAGE_NUMBER, self.ARTICLES_MIN_NUMBER * self.PAGE_STEP_PAGINATION,
                          self.PAGE_STEP_PAGINATION):
            url = self.start_urls[
                      0] + f'/?table_post-list_params=%7B"offset"%3A{page}%2C"filter"%3A%7B"lang"%3A"en"%7D%7D'
            yield scrapy.Request(url, callback=self.parse_page, )

    def parse_page(self, response):
        driver = webdriver.Chrome(self.CHROME_DRIVER_PATH)
        url = response.url
        driver.get(url)
        archive_results = driver.find_elements(By.CLASS_NAME, self.PAGE_ARTICLES_CLASS_NAME)
        for page in archive_results:
            url = page.get_attribute('href')
            yield scrapy.Request(url, callback=self.parse_article)
        driver.quit()

    def parse_article(self, response):
        driver = webdriver.Chrome(self.CHROME_DRIVER_PATH)
        url = response.url
        driver.get(url)
        try:
            date = driver.find_element(By.CSS_SELECTOR, self.ARTICLE_DATE_CSS_SELECTOR)
            links = driver.find_elements(By.CSS_SELECTOR, self.LINK_CSS_SELECTOR)
            labels = driver.find_elements(By.CSS_SELECTOR, self.LABEL_CSS_SELECTOR)
            body = driver.find_element(By.CSS_SELECTOR, self.BODY_CSS_SELECTOR)

            label_data = self.__get_label_data(date, url, links, labels, body)
            self.__validate_label_data(label_data)
            self.create_article(label_data)
        except Exception:
            pass
        driver.quit()

    @staticmethod
    def __valid_links(links):
        article_links = []
        for link in links:
            current_link = link.get_attribute('href')
            if check_valid_link(current_link):
                article_links.append(current_link)
        return article_links

    @staticmethod
    def __validate_label_data(label_data):
        schema = {
            "$schema": "http://json-schema.org/draft-04/schema#",
            'type': 'object',
            'properties': {
                'date': {'type': 'string',
                         },
                'url': {'type': 'string'},
                'labels': {'type': 'array', 'items': [{'type': 'string'}]},
                'links': {'type': 'array', 'items': [{'type': 'string'}]},
                'body': {'type': 'string'},
            },
            'required': ['date', 'url', 'labels', 'body']
        }
        validate(instance=label_data, schema=schema)

    @staticmethod
    def __create_article(item: items.ArticlesItem, db: Session = db):
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
            link_dtos.append((LinkCreateDTO(link=link)))

        return repository.create_article(
            article_dto=article_dto,
            labels=label_dtos,
            links=link_dtos,
            db=db
        )

    def __get_label_data(self, *args):
        date, url, links, labels, body = args
        label_data = {
            'date': date_convert(date.text),
            'url': url,
            'labels': [label.text for label in labels],
            'links': self.__valid_links(links),
            'body': body.text,
        }
        return label_data

    def create_article(self, label_data):
        item = items.ArticlesItem()
        item['date'] = label_data['date']
        item['url'] = label_data['url']
        item['body'] = label_data['body']
        item['labels'] = label_data['labels']
        item['links'] = label_data['links']
        if check_article_existence(db, item['url']):
            self.__create_article(item, db)

# Terminal: scrapy crawl article
# scrapy crawl article -o items.json
