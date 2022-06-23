# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from errno import errorcode
import pymongo 
import mysql 
import logging
from itemadapter import ItemAdapter
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import DropItem
from scrapy.utils import log 


SETTINGS = get_project_settings()

class EstateBotPipeline:
    def process_item(self, item, spider):
        return item


class MySQLPipeline(object): 
    table_name = 'properties'

    conf = {
        'user':SETTINGS['MYSQL_USER'], 
        'password':SETTINGS['MYSQL_PASSWORD'], 
        'database':SETTINGS['MYSQL_DATABASE'], 
        'raise_on_warnings':SETTINGS['MYSQL_RAISE_ON_WARNINGS']
    }
    
    def __init__(self): 
        self.connection = self.mysql_connect() 

    def open_spider(self, spider): 
        print("Spider open")

    def process_item(self, item, spider): 
        print("Saving item into DB...") 
        self.save(dict(item)) 
        return item 

    def close_spider(self, spider): 
        self.mysql_close()

    def mysql_connect(self): 
        try: 
            return mysql.connector.connect(**self.conf) 
        except mysql.connector.Error as Err: 
            if Err.errno == errorcode.ER_ACCESS_DENIED_ERROR: 
                print("Something is wrong with you username or password")  
            elif Err.errno == errorcode.ER_BAD_DB_ERROR: 
                print("Database does not exist.") 

            else: 
                print(Err) 

    def save(self, row): 
        #TODO: Implement this function 
        pass  

    def mysql_close(self): 
        self.connection.close()


class MongoDBPipeline(object): 
    def __init__(self): 
        connection = pymongo.MongoClient(
        SETTINGS['MONGODB_SERVER'], 
        SETTINGS['MONGODB_PORT']
        )

        self.logger = logging.getLogger()

        db = connection[SETTINGS['MONGODB_DB']] 
        self.collections = db[SETTINGS['MONGODB_COLLECTION']]

    def process_item(self, item, spider): 
        valid = True 
        for data in item: 
            if not data: 
                valid = False 
                raise DropItem("Missing {0}!".format(data))

        if valid: 
            self.collections.insert_one(dict(item)) 
            self.logger.info("Property item added to MongoDB dataset..")

        return item

