# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector

class NotConfigured(Exception):pass

class CleaningPipeline(object):
    def process_item(self, item, spider):
        if item["houseSourceCode"]:
            item["mortgage"]=item["mortgage"].strip()
        else:
            DropItem("Missing house source code in %s" % item)
        return item
   
class MysqlPipeline(object):
    def __init__(self,db,user,password,host):
        self.conn=mysql.connector.connect(  db=db,
                                            user=user,
                                            password=password,
                                            host=host,
                                            charset='utf8',
                                            use_unicode=True)
        self.cursor=self.conn.cursor()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS lianjia_db")  #not work
        self.cursor.execute("USE lianjia_db")
        self.cursor.execute("""
					create table if not exists {}(id int unsigned not null primary key auto_increment,
					apartmentLayout char(25) not null,
					constructionArea char(25) not null,
					floorArea char(25) not null,
					houseOrientation char(25),
					decoration char(25),
					elevator char(25),
					layoutStructure char(25),
                    buildingType char(25),
                    buildingStruction char(25),
                    staircasesRatio char(25),
                    useRight char(25),
                    listDate char(25),
                    lastTradeDate char(25),
                    mortgage char(25),
                    houseSourceCode char(25),
                    ownershipTransaction char(25),
                    propertyOwner char(25),
                    area char(25),
                    communityName char(25),
                    totalPrice char(25),
                    unitPrice char(25),
                    district char(25)
                    )
					""".format("lianjia_db"))
                 
    def process_item(self, item, spider):
        query=("""INSERT INTO lianjia_db (apartmentLayout,constructionArea,floorArea,houseOrientation,decoration,elevator,
                                               layoutStructure,buildingType,buildingStruction,staircasesRatio,useRight,listDate,
                                               lastTradeDate,mortgage,houseSourceCode,ownershipTransaction,propertyOwner,area,
                                               communityName,totalPrice,unitPrice,district)
                              VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
        self.cursor.execute(query ,(item["apartmentLayout"],
                                   item["constructionArea"],
                                   item["floorArea"],
                                   item["houseOrientation"],
                                   item["decoration"],
                                   item["elevator"],
                                   item["layoutStructure"],
                                   item["buildingType"],
                                   item["buildingStruction"],
                                   item["staircasesRatio"],
                                   item["useRight"],
                                   item["listDate"],
                                   item["lastTradeDate"],
                                   item["mortgage"],
                                   item["houseSourceCode"],
                                   item["ownershipTransaction"],
                                   item["propertyOwner"],
                                   item["area"],
                                   item["communityName"],
                                   item["totalPrice"],
                                   item["unitPrice"],
                                   item["district"]))
                                   
        self.conn.commit()
        return item
        
    @classmethod
    def from_crawler(cls,crawler):
        db_settings=crawler.settings.getdict("DB_SETTINGS")
        if not db_settings:
            raise NotConfigured
        db=db_settings['db']
        user=db_settings['user']
        password=db_settings['password']
        host=db_settings['host']
        return cls(db,user,password,host)
          
    def open_spider(self,spider):
        pass
    def close_spider(self,spider):
        self.conn.close()
        
class DataVisualizationPipeline(object):
    def __init__(self,db,user,password,host):
        self.conn=mysql.connector.connect(  db=db,
                                            user=user,
                                            password=password,
                                            host=host,
                                            charset='utf8',
                                            use_unicode=True)
        self.cursor=self.conn.cursor()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(db))
        self.cursor.execute("USE {}".fromat(db))
        
    @classmethod
    def from_crawler(cls,crawler):
        db_settings=crawler.settings.getdict("DB_SETTINGS")
        if not db_settings:
            raise NotConfigured
        db=db_settings['db']
        user=db_settings['user']
        password=db_settings['password']
        host=db_settings['host']
        return cls(db,user,password,host)
    container=list()
    def open_spider(self,spider):
        pass
    def close_spider(self,spider):
        self.cursor.execute("SELECT district,communityName,totalPrice,unitPrice FROM lianjia_db")
        data=self.cursor.fetchall()
        unitePrice_list=list(map(lambda i:int(i[3]),data))
        #totalPrice_list=list(map(lambda i:eval(i[2]),data))
        plt.hist(unitePrice_list)
        plt.title("HangZhou real estate unite price distribution")
        plt.xlabel("price:Yuan")
        plt.ylabel("counter")
        plt.show()
        self.conn.close()
    def process_item(self,item,spider):
        return item