# -*- coding: utf-8 -*-
import scrapy


class Spiders2Spider(scrapy.Spider):
    name = "spiders2"
    allowed_domains = ["tutorial.spiders"]
    start_urls = (
        'http://www.tutorial.spiders/',
    )

    def parse(self, response):
        pass
