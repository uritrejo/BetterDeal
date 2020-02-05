import scrapy

class KijijiSpider(scrapy.Spider):

    name = "kijiji"

    start_urls = {
        'https://www.kijiji.ca/'
    }

    def parse(self, response):
        title = response.css('title').extract()

        yield {
            'titleText' : title
        }