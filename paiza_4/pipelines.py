# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline

#DB用ライブラリ
import MySQLdb
from twisted.enterprise import adbapi
import MySQLdb.cursors

class Paiza4Pipeline(object):
    def process_item(self, item, spider):
        return item


class JsonExporterPipleline(object):
    #scrapyのJsonItemExporter使用してjsonのエクスポート
    def __init__(self):
        self.file = open("articleexport.json", 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item=item)
        return item


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            images_path = value['path']
        item["images_path"] = images_path

        return item


#mysql保存
#同期処理
class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', '', 'article_spider', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()


    def process_item(self, item, spider):
        insert_sql = """
        insert into paiza_spider(name,position,income,images,images_path,content,url,url_object_id,create_date)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql, (item['name'], item['position'], item['income'], item['images'],
                                         item['images_path'], item['content'], item['url'], item['url_object_id'],
                                         item['create_date']))
        self.conn.commit()


#mysql保存
#非同期処理    twisted    リンク池
class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )

        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        #twistedで非同期な処理を行う
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 異常処理
        query.addErrback(self.handle_error)


    def handle_error(self,failure):
        #非同期処理のエラーを処理
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql = """
              insert into paiza_spider(name,position,income,images,images_path,content,url,url_object_id,create_date)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
        cursor.execute(insert_sql, (item['name'], item['position'], item['income'], item['images'],
                                         item['images_path'], item['content'], item['url'], item['url_object_id'],
                                         item['create_date']))


