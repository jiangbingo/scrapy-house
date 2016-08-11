#!-*-coding:utf-8-*-

__author__ = 'PD-002'

import os
import json
import scrapy
from hashlib import md5
from tutorial.items import DmozItem, TestItem

class DmozSpider(scrapy.Spider):
    """
        for test
    """
    name = "img"
    allowed_domains = ["img.org"]
    start_urls = ["http://newhouse.fang.com/house/s/"]

    def parse(self, response):
        """
        :param response:
        :return:
        """
        # 查询到每个城市的url
        city_names = response.xpath("//div[@class='city20141104nr']//a/text()").extract()
        city_urls = response.xpath("//div[@class='city20141104nr']//a/@href").extract() 
        for i in range(len(city_names)):
            sel = city_urls[i]
            if sel != self.start_urls[0] and sel[-3:] != "txt":
                response.meta["city"] = city_names[i].strip()
                yield scrapy.Request(sel.strip(), callback=self.second_parse, dont_filter=True,
                                     meta=response.meta.copy())

    def second_parse(self, response):
        """
        :param response:
        :return:
        """
        div_list = response.xpath("//div[@class='newnav20141104nr']/div")
        if len(div_list) <= 0:
            return
        # 新房分类url
        type_urls = div_list[3].xpath("div[@class='listBox']/ul//li/a/@href").extract()[:5]
        type_names = div_list[3].xpath("div[@class='listBox']/ul//li/a/text()").extract()[:5]
        for i in range(len(type_names)):
            url = type_urls[i]
            response.meta["type"] = type_names[i].strip()
            if url != response.url and url[-3:] != "txt":
                yield scrapy.Request(url.strip(), callback=self.page_parse, dont_filter=True, meta=response.meta.copy())
        # # 二手房url
        # for url in div_list[4].xpath("div[@class='listBox']/ul//li/a/@href").extract()[:2]:
        #     item = TestItem()
        #     item["url"] = url
        #     if url != response.url and url[-3:] != "txt":
        #         # yield item
        #         yield scrapy.Request(url, callback=self.page_parse, dont_filter=True)
        # 写字楼url
        # for url in div_list[8].xpath("div[@class='listBox']/ul//li/a/@href").extract():
        #     item = TestItem()
        #     item["url"] = url
        #     if url != response.url and url[-3:] != "txt":
        #         # yield item
        #         yield scrapy.Request(url, callback=self.page_parse, dont_filter=True)

    def page_parse(self, response):
        """
        :param response:
        :return:
        """
        # 分页
        a_list = response.xpath("//a")
        page_url = None
        for a in a_list:
            text = a.xpath("text()").extract()
            if len(text) > 0 and ("末页".decode("utf-8") in text[0] or "尾页".decode("utf-8") in text[0]):
                page_url = self._find_page_url(a.xpath("@href").extract()[0])
                break
        if page_url:
            for a in a_list:
                hrefs = a.xpath("@href").extract()
                if len(hrefs) > 0:
                    href = hrefs[0]
                    if page_url in href:
                        new_page_url = response.urljoin(href)
                        if new_page_url[-3:] != "txt":
                            yield scrapy.Request(new_page_url.strip(), self.detail_page_parse, dont_filter=True,
                                                 meta=response.meta.copy())

    def detail_page_parse(self, response):
        """
        :param response:
        :return:
        """
        url_list = response.xpath("//strong[@class='f14 fb_blue']/a/@href").extract()
        if len(url_list) <= 0:
            url_list = response.xpath("//div[@class='nlcd_name']/a/@href").extract()
        if len(url_list) <= 0:
            cache_list = response.xpath("//dd[@class='info rel floatr']/p[@class='title']/a/@href").extract()
            for cache in cache_list:
                url_list.append(response.urljoin(cache.strip()))
        if len(url_list) > 0:
            for url in url_list:
                if "http" not in url:
                    url = response.urljoin(url)
                url = url.strip()
                city = response.meta["city"].replace(" ", "")
                type_name = response.meta["type"].replace(" ", "")
                dir_name = os.path.join(os.path.dirname(os.path.abspath("img_spiders.py")), "imgs", type_name,
                                        city, url.split("/")[2])
                if not os.path.exists(dir_name):
                    response.meta["dir_name"] = dir_name
                    yield scrapy.Request(url, self.find_img_page_parse, dont_filter=True, meta=response.meta.copy())

    def find_img_page_parse(self, response):
        """
        :param response:
        :return:
        """
        texts = response.xpath("//div[@class='navleft tf']//a[5]/text()").extract()
        if len(texts) > 0:
            if "户型图".decode("utf-8") == texts[0]:
                page_urls = response.xpath("//div[@class='navleft tf']//a[5]/@href").extract()
            else:
                page_urls = response.xpath("//div[@class='navleft tf']//a[6]/@href").extract()
            if len(page_urls) > 0:
                page_url = page_urls[0]
                yield scrapy.Request(page_url.strip(), self.find_img_url_parse, dont_filter=True,
                                     meta=response.meta.copy())
        else:
            return

    def find_img_url_parse(self, response):
        """
        :param response:
        :return:
        """
        img_urls = response.xpath("//ul[@class='by_img_list my_ul clearfix']//li/a/img/@src").extract()
        names = response.xpath("//ul[@class='by_img_list my_ul clearfix']//li/a/p/text()").extract()
        msgs = response.xpath("//li[@class='xx_list']")
        if len(msgs) == 6:
            if len(names) <= 0:
                return
            try:
                mo = md5()
                mo.update(names[0].encode("utf-8"))
                img_name = mo.hexdigest()
                dir_name = response.meta["dir_name"]
                if not os.path.exists(dir_name):
                    os.makedirs(dir_name)
                config = {"img_name": img_name}
                types = msgs[0].xpath("em/text()").extract()
                if len(types) > 0:
                    config["type"] = types[0].strip()
                hxfbs = msgs[1].xpath("em/text()").extract()
                if len(hxfbs) > 0:
                    config["hxfb"] = hxfbs[0].strip()
                jzmjs = msgs[2].xpath("em/i/text()").extract()
                if len(jzmjs) > 0:
                    config["jzmj"] = jzmjs[0].strip()
                jjs = msgs[3].xpath("em/i/text()").extract()
                if len(jjs) > 0:
                    config["jj"] = jjs[0].strip()
                zjs = msgs[5].xpath("em/i/text()").extract()
                if len(zjs) > 0:
                    config["zj"] = zjs[0].strip()
                apartment_names = response.xpath("//div[@class='img_num fl']/strong/text()").extract()
                if len(apartment_names) > 0:
                    config["apartment_name"] = apartment_names[0].strip()
                file_name = os.path.join(dir_name, "config.txt")
                fd = open(file_name, "w+")
                fd.write(json.dumps(config))
                fd.close()
                url = img_urls[0].replace("124x82", "880x578")
                response.meta["img_name"] = img_name
                yield scrapy.Request(url.strip(), self.load_img, dont_filter=True, meta=response.meta.copy())
            except:
                import ipdb;ipdb.set_trace()
        else:
            print "find_img_url_parse error", response.url

    def load_img(self, response):
        """
        :param response:
        :return:
        """
        dir_name = response.meta["dir_name"]
        file_name = os.path.join(dir_name, response.meta["img_name"] + ".jpg")
        with open(file_name, "wb+") as fd:
            fd.write(response.body)

    def _find_page_url(self, url):
        """
        :param url:
        :return:
        """
        flag = "?page="
        if url.find(flag) > 0:
            return url.split("?page=")[0]
        else:
            a_list = url.split("/")[1:-2]
            new_url = "/"
            for i in a_list:
                new_url = new_url + i + "/"
            return new_url