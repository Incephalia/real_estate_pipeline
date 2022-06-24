import time 

from scrapy import Spider 
from estatebot.items import Property24Item 



class Property24Spider(Spider): 
    name = 'property24' 
    download_delay = 5.0
    start_urls = [
        'https://www.property24.com/for-sale/cape-town/western-cape/432/p22', 
    ] 

    def parse(self, response): 
        #time.sleep(3)
        for property in response.css('div.js_resultTile'):
            item = Property24Item() 

            item['name'] = property.css('::attr(title)').get()  
            item['price'] = property.css('div.p24_price::text').get().replace("\r\n", "")
            item['location'] = property.css('span.p24_location::text').get()
            size_selector = property.css('span.p24_size')
            item['size'] = size_selector.xpath('.//span/text()').get().replace("m\u00b2", "(sq m)")
            item['image'] = property.css('img.js_rollover_target::attr(src)').get() 

            yield item

        next_page_top = response.css('div.p24_pager')
        next_page = next_page_top.css('a.pull-right::attr(href)')

        if next_page is not None: 
            #time.sleep(1)
            yield response.follow(next_page.get(), self.parse)


    