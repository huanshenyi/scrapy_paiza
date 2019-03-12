# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline


class Paiza4Pipeline(object):
    def process_item(self, item, spider):
        return item


class JsonExporterPipleline(object):
    #scrapyのJsonItemExporter使用してjsonのエクスポート
    def __init__(self):
        self.file = open("articleexport.json", 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self,spider):
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
