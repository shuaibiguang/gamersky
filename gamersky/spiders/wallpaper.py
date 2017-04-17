# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from gamersky.items import WallpaperItem, WallpaperLoaderItem

class WallpaperSpider(scrapy.Spider):
    name = "wallpaper"
    allowed_domains = ["www.gamersky.com/ent/wp/"]
    start_urls = ['http://www.gamersky.com/ent/wp/']


    def parse(self, response):
        home_list_url = response.xpath('//ul[contains(@class,"contentpaging")]/li//div[@class="tit"]/a/@href').extract()
        for home_url in home_list_url:
            url = parse.urljoin(response.url, home_url)
            yield Request(url=url, callback=self.two_parse, dont_filter=True)

    # 拿取下一页连接从新拿取首页的列表页进行爬取, 算了这个下一页是js生成的，以后技术到位在翻页把


    def two_parse(self, response):
        # 首先拿取图片的链接地址，传递下去
        two_list_url = response.xpath('//div[@class="Mid2L_con"]//p[@align="center"]/a/@href').extract()
        action_wall = WallpaperItem()
        for two_url in two_list_url:
            wallLoaderItem = WallpaperLoaderItem(item=WallpaperItem(), response=response)
            wallLoaderItem.add_value('wall_img', two_url)
            action_wall = wallLoaderItem.load_item()
            yield action_wall

    #     拿取下一页继续进行爬取
        next_url = response.xpath('//div[@class="page_css"]/a/@href').extract()[-1]
        if next_url != response.url:
            yield Request(parse.urljoin(response.url, next_url), callback=self.two_parse, dont_filter=True)
