import scrapy

class KijijiSpider(scrapy.Spider):

    # later a hash map could optimize search
    cars = []
    prices = []
    removedPrices = [] # temporary, just to see the amount of prices that are being removed

    round = 0

    name = "kijiji"
    start_urls = {
        # 'https://www.kijiji.ca/b-ontario/honda-civic/k0l9004?dc=true' #Ontario
        'https://www.kijiji.ca/b-cars-trucks/ottawa-gatineau-area/honda-civic/k0c174l1700184' #Ottawa
    }

    def parse(self, response):

        print("Starting round of collection.")

        extractedCars = response.css('.title .title::text').extract() # gets the car add titles using css selectors
        extractedPrices = response.css('.price::text').extract() # gets the prices

        # the original strings contain a huge amount of unnecessary white characters, so we'll strip them and add them here
        strippedExtractedCars = []
        strippedExtractedPrices = []

        # print("\n1\n")

        # first we strip every string in both lists:

        for car in extractedCars:
            strippedCar = car.strip()
            strippedExtractedCars.append(strippedCar)

            if(len(strippedCar)==0):
                print("\n******A CAR WAS EMPTY!\n")

        # print("\n2\n")

        # within prices, not all of the strings are relevant, a lot of "fake values" are returned, '
        # so we have to clean the list and only re-add the valid prices
        for price in extractedPrices:
            strippedPrice = price.strip()

            if(len(strippedPrice) == 0):
                # print("Zero len priceee")
                self.removedPrices.append(strippedPrice)
            # apparently all of the ones that aren't prices are just blank spaces bro
            # elif('$' not in strippedPrice):
            #     print("No $ inside")
            #     self.removedPrices.append(strippedPrice)
            else:
                strippedExtractedPrices.append(strippedPrice)

        # print("\n3\n")

        # now we check onto our global list if the given car extracted had already been processed
        # if it hadn't, then we send a notification (print for now lol)

        if(len(strippedExtractedCars) == len(strippedExtractedPrices)):

            # we check if it's new, we print the new ones
            # if new, we add both the car and the price
            # we could also add a counter to avoid notifying within the first rounds

            for i in range(0, len(strippedExtractedCars)):

                newCar = strippedExtractedCars[i]
                carPrice = strippedExtractedPrices[i]

                if(newCar not in self.cars): # if it's a new posting, we notify and we add it

                    print("New Car:\n", newCar, "\n", carPrice)
                    self.cars.append(newCar)
                    self.prices.append(carPrice)

        else: # we have a different number of cars and prices, we can't compare
            print("\nTragedie:\nStripped Cars: ", len(strippedExtractedCars), "\nStripped Prices: ", len(strippedExtractedPrices))

        # print("Removed Prices len: ", len(self.removedPrices))


        self.removedPrices.clear() # it was just to see the amount, long way lol

        print("Round Finished.")
        round += 1

        yield {
            'car_adds' : extractedCars,
            'prices' : extractedPrices
        }