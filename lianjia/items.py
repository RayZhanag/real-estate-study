# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class LianjiaItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    apartmentLayout=Field()         #房屋户型
    constructionArea=Field()        #建筑面积
    floorArea=Field()               #套内面积
    houseOrientation=Field()        #朝向
    decoration=Field()                 #装修
    elevator=Field()                  #电梯
    layoutStructure=Field()         #even level;jump layer;duplicate
    buildingType=Field()            #建筑类型
    buildingStruction=Field()      #建筑结构
    staircasesRatio=Field()        #梯户比
    useRight=Field()               #产权年限
    listDate=Field()               #挂牌时间
    lastTradeDate=Field()          #上次交易
    mortgage=Field()              #抵押信息
    houseSourceCode=Field()       #房源编码
    ownershipTransaction=Field()  #交易权属
    propertyOwner=Field()         #产权所属
    area=Field()                  #所在区域
    communityName =Field()        #小区名称
    totalPrice=Field()            #总价
    unitPrice=Field()             #单价
    district=Field()              #所在区县
    
