import time

from scrapy import Spider 
from estatebot.items import PropertyItem
from scrapy.loader import ItemLoader
from estatebot.utils.constants import property_co_za_endpoints





class PropertySpider(Spider): 
    name = 'property' 
    start_urls = [ 
         #'https://www.privateproperty.co.za/commercial-sales/western-cape/cape-town/atlantic-seaboard/1683',
         'https://www.privateproperty.co.za/bank-sales/western-cape/4?page=2',
    ] + property_co_za_endpoints 

    def parse(self, response): 
        #time.sleep(3)
        for property in response.css('a.listingResult'): 
            # l = ItemLoader(item=PropertyItem(), selector=property) 

            # l.add_css('name', 'div.title') 
            # l.add_css('price', 'div.priceDescription') 
            # l.add_css('price_additional_description', 'div.priceAdditionalDescriptior')
            # l.add_css('property_type', 'div.propertyType') 
            # l.add_css('suburb', 'div.suburb') 
            # l.add_css('bank_or_private', 'div.bankOfficeOrPrivateSeller')
            # l.add_css('seller', 'div.agentBankOrPrivateSellerName') 
            item = PropertyItem() 

            item['name'] = property.css('div.title::text').get().replace('m\u00b2', '(sq m)') 
            item['price'] = property.css('div.priceDescription::text').get() 
            item['price_additional_description'] = property.css('div.priceAdditionalDescriptor::text').get() 
            item['property_type'] = property.css('div.propertyType::text').get() 
            item['suburb'] = property.css('div.suburb::text').get() 
            item['bank_or_private'] = property.css('div.bankOfficeOrPrivateSeller::text').get().replace('\r\n', '') 
            item['seller_or_status'] = property.css('div.agentBankOrPrivateSellerName::text').get().replace('\r\n', '') if property.css('div.agentBankOrPrivateSellerName::text').get() else None 
            item['property_images'] = property.css('img::attr(data-src)').get() 

            yield item        

            # yield {
            #     'name': property.css('div.title::text').get().replace('m\u00b2', '(sq m)'), 
            #     'price': property.css('div.priceDescription::text').get(), 
            #     'price_additional_description': property.css('div.priceAdditonalDescriptor::text').get(), 
            #     'property_type': property.css('div.propertyType::text').get(), 
            #     'suburb': property.css('div.suburb::text').get(), 
            #     'bank_or_private': property.css('div.bankOfficeOrPrivateSeller::text').get().replace('\r\n', ''), 
            #     'seller_or_status': property.css('div.agentBankOrPrivateSellerName::text').get().replace('\r\n', ''), 
            #     'images': property.css('img::attr(data-src)').get()
            # }

        next_page = response.css('a.pageNumber.clear::attr(href)')
        if next_page is not None: 
            #time.sleep(2)
            yield response.follow(next_page[0].extract(), self.parse)


