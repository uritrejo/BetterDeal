import scrapy
# import notification.email_config
import notification.notification_manager
# from dataExtraction.dataCollector import *
import dataExtraction.dataCollector
import config

class KijijiSpider(scrapy.Spider):


    name = "kijiji"
    start_urls = config.LINKS_TO_SCRAPE

    def parse(self, response):

        print("Starting round of collection: ", dataExtraction.dataCollector.round)

        extractedCars = response.css('.title .title::text').extract() # gets the car add titles using css selectors
        extractedPrices = response.css('.price::text').extract() # gets the prices

        # the original strings contain a huge amount of unnecessary white characters, so we'll strip them and add them here
        strippedExtractedCars = []
        strippedExtractedPrices = []

        # first we strip every string in both lists to get the list of prices aligned with their ad

        for car in extractedCars:
            strippedCar = car.strip().strip('"') # we erase the whitespaces and the "" surrounding the name
            strippedExtractedCars.append(strippedCar)
            if(len(strippedCar)==0):
                print("\n******A CAR WAS EMPTY!\n")

        # within prices, not all of the strings are relevant, a lot of "fake values" are returned, '
        # so we have to clean the list and only re-add the valid prices
        for price in extractedPrices:
            strippedPrice = price.strip().strip('"')
            if(len(strippedPrice) != 0): # there are some "fake" prices that need to be removed, they're pure whitespaces
                strippedExtractedPrices.append(strippedPrice)

        # now that we cleaned the data, we can send it to the dataCollector
        dataExtraction.dataCollector.processNewData(strippedExtractedCars, strippedExtractedPrices)

        print("Round Finished.")

        dataExtraction.dataCollector.round += 1

        dataExtraction.dataCollector.exportDataToCSV()

        # yield {
        #     'car_adds' : extractedCars,
        #     'prices' : extractedPrices
        # }