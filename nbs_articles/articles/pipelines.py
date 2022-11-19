# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import sqlite3


class ArticlesPipeline:
    pass
    # def __init__(self):
    #     self.create_connection()
    #
    # def create_connection(self):
    #     self.connect = sqlite3.connect('articles_db')
    #     self.cursor = self.connect.cursor()
    #
    # def process_item(self, item, spider):
    #     self.store_db(item)
    #     return item
    #
    # def store_db(self, item):
    #     self.cursor.execute("""select * from articles where url = ?""", (item['url'],))
    #     result = self.cursor.fetchone()
    #
    #     if not result:
    #         self.cursor.execute("""insert into articles (url, date, body) value (?, ?, ?)""",
    #                             (item['url'], item['date'], item['body'])
    #                             )
    #         # for label in item['labels']:
    #         #     self.cursor.execute("""insert into labels (label, article_id) value (?,?)""",
    #         #                         (label, id))
    #         #
    #         # for link in item['links']:
    #         #     self.cursor.execute("""insert into links (link, article_id) value (?,?)""",
    #         #                         (link, id))
    #
    #         self.connect.commit()
