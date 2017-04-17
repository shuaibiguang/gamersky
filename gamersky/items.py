# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst

class GamerskyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# 这这里做loaderItem 做默认限制
class WallpaperLoaderItem(ItemLoader):
    default_output_processor = TakeFirst()

def get_img_down(value):
    return value.split('?')[-1]

# 解决first冲突，下载图片需要使用list
def return_value(value):
    return [value]


class WallpaperItem(scrapy.Item):
    wall_img = scrapy.Field(
        input_processor = MapCompose(get_img_down),
        output_processor = MapCompose(return_value)
    )