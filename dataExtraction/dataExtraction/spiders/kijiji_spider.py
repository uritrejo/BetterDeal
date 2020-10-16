import scrapy
# import notification.notification_manager
import dataExtraction.dataCollector
import config
# import database.database as db


class KijijiSpider(scrapy.Spider):

    name = "kijiji"
    start_urls = config.LINKS_TO_SCRAPE
    # start_urls = db.retrieveSearches()

    def parse(self, response):

        print("Starting round of collection: ", dataExtraction.dataCollector.round)

        extractedCars = response.css('.title .title::text').extract()  # gets the car add titles using css selectors
        extractedPrices = response.css('.price::text').extract()  # gets the prices
        extractedLinks = response.css('.title::attr(href)').extract()  # gets the link to the given posting

        print("About to cal stripp with len: ", len(extractedCars))

        # the original strings contain a huge amount of unnecessary white characters, so we'll strip them and add them here
        strippedExtractedCars = []
        strippedExtractedPrices = []
        strippedExtractedLinks = []

        # first we strip every string in all lists to get the list of prices aligned with their posting and link
        for car in extractedCars:
            strippedCar = car.strip().strip('"') # we erase the whitespaces and the "" surrounding the name
            strippedExtractedCars.append(strippedCar)
            if(len(strippedCar)==0):
                print("\n******A CAR WAS EMPTY!\n")

        # within prices, not all of the strings are relevant, a lot of "fake values" are returned, '
        # so we have to clean the list and only re-add the valid prices
        for price in extractedPrices:
            strippedPrice = price.strip().strip('"')  # here add .strip('$').strip(',')
            if(len(strippedPrice) != 0): # there are some "fake" prices that need to be removed, they're pure whitespaces
                strippedExtractedPrices.append(strippedPrice)

        for link in extractedLinks:
            strippedLink = link.strip().strip('"') # we erase the whitespaces and the "" surrounding the name
            strippedExtractedLinks.append(strippedLink)
            if(len(strippedLink)==0):
                print("\n******A LINK WAS EMPTY!\n")


        print("About to cal collector with len: ", len(strippedExtractedCars))


        # now that we cleaned the data, we can send it to the dataCollector
        dataExtraction.dataCollector.processNewData(strippedExtractedCars, strippedExtractedPrices, strippedExtractedLinks)

        print("Round Finished.")

        # collector.round += 1

        # not calling it anymore now that we have Firebase
        # collector.exportDataToCSV()