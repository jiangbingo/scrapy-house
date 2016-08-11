#!-*-coding:utf-8-*-

__author__ = 'PD-002'

import json
import os
import re
import scrapy
from tutorial.items import DmozItem, TestItem

class DmozSpider(scrapy.Spider):
    """
        for test
    """
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = ["http://newhouse.fang.com/house/s/"]
    urls = []

    def init(self):
        """
        :return:
        """
        file_path = os.path.join(os.path.dirname(os.path.abspath("dmoz_spider.py")), "urls.json")
        fd = open(file_path, "r")
        self.urls = json.loads(fd.read())
        fd.close()
        print "-------length------", len(self.urls)

    def parse(self, response):
        """
        :param response:
        :return:
        """
        # 查询到每个城市的url
        self.init()
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
                response.meta["page"] = url
                shot_url = url.replace(" ", "").split("/")[2]
                if shot_url not in self.urls:
                    self.urls.append(shot_url)
                    yield scrapy.Request(url, self.find_detail_parse, dont_filter=True, meta=response.meta.copy())
                # else:
                #     print "existed", url

    def find_detail_parse(self, response):
        """
        :param response:
        :return:
        """
        detail_pages = response.xpath("//div[@class='fl more']/p/a/@href").extract()
        if len(detail_pages) > 0:
            detail_page = detail_pages[0]
            yield scrapy.Request(detail_page.strip(), self.message_parse, dont_filter=True, meta=response.meta.copy())

    def message_parse(self, response):
        """
        :param response:
        :return:
        """
        tr_list = response.xpath("//div[@class='besic_inform']/table//tr")
        if len(tr_list) >= 12:
            item = DmozItem()
            item["url"] = response.meta["page"].replace(" ", "").split("/")[2]
            item["name"] = response.xpath("//div[@class='lpbt tf jq_nav']/h1/a/text()").extract()[0]
            item["location"] = "/".join(response.xpath("//div[@class='header_mnav']/p//a/text()").extract())
            line1 = tr_list[0]
            values1 = line1.xpath("td/text()").extract()
            item["wylb"] = values1[0].strip()
            item["xmts"] = values1[1].strip()
            line2 = tr_list[1]
            values2 = line2.xpath("td/text()").extract()
            item["jzlb"] = values2[0].strip()
            item["zxzk"] = values2[1].strip()
            line3 = tr_list[2]
            hxwz = line3.xpath("td/span/a/text()").extract()
            if len(hxwz) > 0:
                item["hxwz"] = hxwz[0].strip()
            zxal = line3.xpath("td/span/a/text()").extract()
            if len(zxal) > 0:
                item["zxal"] = zxal[0].strip()
            line4 = tr_list[3]
            values4 = line4.xpath("td/text()").extract()
            item["rjl"] = values4[0].strip()
            item["lhl"] = values4[1].strip()
            line5 = tr_list[4]
            values5 = line5.xpath("td/text()").extract()
            item["kpsj"] = values5[0].strip()
            item["jfsj"] = values5[1].strip()
            line6 = tr_list[5]
            item["wyf"] = line6.xpath("td/text()").extract()[0].strip()
            wygs = line6.xpath("td/span/a/text()").extract()
            if len(wygs) > 0:
                item["wygs"] = wygs[0].strip()
            kfs = tr_list[6].xpath("td/span/a/text()").extract()
            if len(kfs) > 0:
                item["kfs"] = kfs[0].strip()
            item["ysxkz"] = tr_list[7].xpath("td/text()").extract()[0].strip()
            item["sldz"] = tr_list[8].xpath("td/text()").extract()[0].strip()
            item["wydz"] = tr_list[9].xpath("td/text()").extract()[0].strip()
            item["jtzk"] = tr_list[10].xpath("td/text()").extract()[0].strip()
            price = tr_list[11].xpath("td/span/strong/text()").extract()
            value = None
            if len(price) > 0:
                names = tr_list[11].xpath("td/span/text()").extract()
                if len(names) >= 2:
                    value = names[0].strip() + price[0].strip() + names[1].strip()
            item["fj"] = value
            item["city"] = response.meta["city"].replace(" ", "")
            item["type_name"] = response.meta["type"].replace(" ", "")
            msgs = response.xpath("//div[@class='lineheight']").extract()
            if len(msgs) > 0:
                msg = msgs[-1].replace("\n", "")
                keys = re.findall(r"<strong>(.*?)</strong>", msg)
                values = re.findall(r"</strong>(.*?)<br>", msg)
                count = len(keys)
                if len(values) == count:
                    for i in range(count):
                        key = keys[i]
                        if "占地面积".decode("utf-8") in key:
                            item["zdmj"] = values[i].strip()
                        elif "建筑面积".decode("utf-8") in key:
                            item["jzmj"] = values[i].strip()
                        elif "开工时间".decode("utf-8") in key:
                            item["kgsj"] = values[i].strip()
                        elif "竣工时间".decode("utf-8") in key:
                            item["jgsj"] = values[i].strip()
                        elif "产权年限".decode("utf-8") in key:
                            nx = re.search(r"(\d+)", values[i]).group()
                            item["cqnx"] = nx
            yield item

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
