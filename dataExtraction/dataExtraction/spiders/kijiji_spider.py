import scrapy

class KijijiSpider(scrapy.Spider):

    cars = [] #later a hash map could optimize search

    name = "kijiji"
    start_urls = {
        # 'https://www.kijiji.ca/b-ontario/honda-civic/k0l9004?dc=true' #Ontario
        'https://www.kijiji.ca/b-cars-trucks/ottawa-gatineau-area/honda-civic/k0c174l1700184' #Ottawa
    }

    def parse(self, response):

        car_ad_titles = response.css('.title .title::text').extract() # gets the car add titles using css selectors

        prices = response.css('.price::text').extract()

        print("Starting round of collection.")

        for car in car_ad_titles:

            if car not in self.cars:

                print("New Car:")
                print(car)
                self.cars.append(car)

        # problem: the cars array and the prices array are of different lengths
        # so idk how I'm gonna map the prices to the car
        # Maybe if i use the blocks like the guy in the video it makes it easier, there has to be a way
        print("Size of cars array: ", len(self.cars))
        # print("Size of cars array: ", len(car_ad_titles))
        # print("Size of prices array: ", len(prices))


        yield {
            'car_adds' : car_ad_titles,
            'prices' : prices
        }