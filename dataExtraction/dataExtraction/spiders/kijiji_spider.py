import scrapy

class KijijiSpider(scrapy.Spider):

    name = "kijiji"
    start_urls = {
        'https://www.kijiji.ca/b-ontario/honda-civic/k0l9004?dc=true'
    }

    def parse(self, response):

        car_ad_titles = response.css('.title .title::text').extract()

        prices = response.css('.price::text').extract()

        print("Starting round of collection.")

        for car in car_ad_titles:
            print(car)


        yield {
            'car_adds' : car_ad_titles,
            'prices' : prices
        }