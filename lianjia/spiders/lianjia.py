# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.spiders import CrawlSpider,Rule
#from scrapy.loader import ItemLoader
from lianjia.items import LianjiaItem
from scrapy.linkextractors import LinkExtractor
from scrapy import Spider,Selector
import scrapy,logging,re


logger = logging.getLogger('LianJia')             
class LianjiaSpider(Spider):
    
    name='lianjia'
    #allowed_domains=["hz.lianjia.com/ershoufang"]
    start_urls=["https://hz.lianjia.com/ershoufang/"]
    
    def __init__(self):
        self.main_url="https://hz.lianjia.com"
        self.current_url="https://hz.lianjia.com/ershoufang/pg"

    #response.css("ul.sellListContent li.clear div.info.clear div.title a::attr('href')").extract()
    def parse(self,response):
        links=response.css("div.position div[data-role=ershoufang] div a::attr('href')").extract()
        zone_urls=map(lambda item: self.main_url+item, links)
        for url in zone_urls:
            yield scrapy.Request(url,callback=self.parse_zone)

    def parse_zone(self,response):
        def get_page_number_range(response):
            str_of_dict=response.xpath("//div/div[@page-data]/@page-data").extract_first() #put it inside "try" to let it seems comfortable.
            page_dict=eval(str_of_dict)
            total_page=page_dict.get("totalPage")
            return total_page

        total_page=get_page_number_range(response)
        #parse current/first page
        self.parse_page(response)
        for i in range(2,1+total_page):
            yield scrapy.Request(response.url+"pg"+str(i),self.parse_page)
            
    def parse_page(self,response):
        urls=response.css("ul.sellListContent li.clear div.info.clear div.title a::attr('href')").extract()
        for url in urls:
            yield scrapy.Request(url,callback=self.parse_content)  #visit every house source  

    def parse_content(self,response):
        logger.info("visit page: " + response.url)
        baseProperty=response.css("div.introContent div.base div.content ul li::text").extract() #基本属性
        transactionProperty=response.css("div.introContent  div.transaction div.content ul li span:nth-child(2)::text ").extract()#交易属性
        district,area=response.css("div.aroundInfo div.areaName span.info a::text").extract()
        communityName=response.css("div.overview div.content div.aroundInfo div.communityName a.info::text").extract_first()
        totalPrice=response.css("div.price span.total::text").extract_first()
        unitPrice=response.css("div.price div.text div.unitPrice span.unitPriceValue::text").extract_first()
        if len(transactionProperty) == 9 and len(baseProperty)== 12:
            LianJia=LianjiaItem()
            LianJia["apartmentLayout"]=baseProperty[0]         #房屋户型
            LianJia["constructionArea"]=baseProperty[2]        #建筑面积
            LianJia["floorArea"]=baseProperty[4]              #套内面积
            LianJia["houseOrientation"]=baseProperty[6]        #朝向
            LianJia["decoration"]=baseProperty[8]                 #装修
            LianJia["elevator"]=baseProperty[10]                 #电梯
            LianJia["layoutStructure"]=baseProperty[3]        #even level;jump layer;duplicate
            LianJia["buildingType"]=baseProperty[5]           #建筑类型
            LianJia["buildingStruction"]=baseProperty[7]      #建筑结构
            LianJia["staircasesRatio"]=baseProperty[9]        #梯户比
            LianJia["useRight"]=baseProperty[11]              #产权年限
            LianJia["listDate"]=transactionProperty[0]              #挂牌时间
            LianJia["lastTradeDate"]=transactionProperty[2]         #上次交易
            LianJia["mortgage"]=transactionProperty[6]           #抵押信息
            LianJia["houseSourceCode"]=transactionProperty[8]       #房源编码
            LianJia["ownershipTransaction"]=transactionProperty[1]  #交易权属
            LianJia["propertyOwner"]=transactionProperty[5]        #产权所属
            LianJia["area"]=area                                   #所在区域
            LianJia["communityName"]=communityName                 #小区名称
            LianJia["totalPrice"]=  totalPrice                     #总价
            LianJia["unitPrice"]=  unitPrice                       #单价
            LianJia["district"]= district                          #所在区县
            yield LianJia
        else:
            pass

            
  

        

            
      