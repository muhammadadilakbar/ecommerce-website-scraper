import scrapy
from marketorganics.items import MarketorganicsItem

class MospiderSpider(scrapy.Spider):
    name = 'moSpider'
    allowed_domains = ['marketorganics.com.au']
    start_urls = [ 'https://shop.marketorganics.com.au/category/alcohol',
    'https://shop.marketorganics.com.au/category/baby',
    'https://shop.marketorganics.com.au/category/bakery-bread',
    'https://shop.marketorganics.com.au/category/clothing-3-buy-discount',
    'https://shop.marketorganics.com.au/category/freezer-3-buy-discount',
    'https://shop.marketorganics.com.au/category/fridge-3-buy-discount',
    'https://shop.marketorganics.com.au/category/produce',
    'https://shop.marketorganics.com.au/category/garden-products',
    'https://shop.marketorganics.com.au/category/grocery-6-buy-discount',
    'https://shop.marketorganics.com.au/category/household-3-buy-discount',
    'https://shop.marketorganics.com.au/category/pet-3-buy-discount',
    'https://shop.marketorganics.com.au/category/pharmacy-3-buy-discount',
    'https://shop.marketorganics.com.au/category/bulk-products',
    'https://shop.marketorganics.com.au/category/butcher-1',
    'https://shop.marketorganics.com.au/category/bulk-bins',
    'https://shop.marketorganics.com.au/category/dairy',
    'https://shop.marketorganics.com.au/category/beverages',
     ]

    def parse(self, response):
        category = response.url.split('/')[-1]
        if category.find('?') != -1:
            queryStringIndex = category.find('?')
            category = category[0:queryStringIndex]
        products = response.xpath( '/descendant::div[attribute::class="TalkerGrid__Item"]' )
        for product in products:
            product_name = product.xpath( './descendant::div[attribute::class="talker__name talker__section"]/attribute::title' ).get()
            product_price = product.xpath( './descendant::strong[attribute::class="price__sell"]/text()' ).get()
            item = MarketorganicsItem()
            item['product_name'] = product_name
            item['product_price'] = product_price[1:]
            item['category'] = category
            yield item
        try:
            next_page = response.xpath( '//a[attribute::class="next_page"]/attribute::href' ).extract()[0]
            yield response.follow( next_page, callback=self.parse )
        except IndexError:
            self.log( "Finished parsing URL: %s" % response.url )

