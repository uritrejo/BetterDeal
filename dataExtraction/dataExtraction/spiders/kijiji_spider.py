import scrapy
import database.database as db
import dataExtraction.dataCollector as collector
import config
import traceback
import logging

# we get the logger
logger = logging.getLogger("BetterDealer")

class KijijiSpider(scrapy.Spider):

    name = "kijiji"
    # start_urls = [  # for testing
    #     'https://www.kijiji.ca/b-cars-trucks/ottawa-gatineau-area/gmc-yukon/2016__/k0c174l1700184a68', # GMC Yukon > 2016
    #     'https://www.kijiji.ca/b-cars-trucks/ottawa-gatineau-area/dodge-ram-rebel/2019__/k0c174l1700184a68' # Dodge RAM Rebel 2019-2020]  # for testing
    #     ]
    start_urls = db.retrieveSearches()

    # needed to bypass initial request issues
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'COOKIES_ENABLED': False,
        'BOT_NAME': 'betterFinder',
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
        }
    }

    def parse(self, response):

        '''
            I can make a dictionary to keep count for each car individually, otherwise, that
            is gonna be a problem whenever I'm adding new cars on the go, it's gonna email bomb
            da fok outta every email.
            response.request.url has the link, from there i should be able to do it
        '''

        currentRequestURL = response.request.url
        collector.updateSearchesCount(self.start_urls)
        # print("Starting round ", collector.searchRounds[currentRequestURL],
        #       " of collection for: ", currentRequestURL)

        logger.info("Starting round " + str(collector.searchRounds[currentRequestURL]) +
              " of collection for: " + str(currentRequestURL))

        extractedCars = response.css('.title .title::text').extract()  # gets the car add titles using css selectors
        extractedPrices = response.css('.price::text').extract()  # gets the prices
        extractedLinks = response.css('.title::attr(href)').extract()  # gets the link to the given posting

        #  the original strings contain a huge amount of unnecessary white characters,
        #  so we'll strip them and add them here
        strippedExtractedCars = []
        strippedExtractedPrices = []
        strippedExtractedLinks = []

        # print("Lengths of lists: ", len(extractedCars), len(extractedPrices), len(extractedLinks))

        # first we strip every string in all lists to get the list of prices aligned with their posting and link
        for car in extractedCars:
            strippedCar = car.strip().strip('"')  # we erase the whitespaces and the "" surrounding the name
            strippedExtractedCars.append(strippedCar)
            if len(strippedCar) == 0:
                print("\n******A CAR WAS EMPTY!\n")

        # within prices, not all of the strings are relevant, a lot of "fake values" are returned, '
        # so we have to clean the list and only re-add the valid prices
        for price in extractedPrices:
            strippedPrice = price.strip().strip('"')  # here add .strip('$').strip(',')
            if len(strippedPrice) != 0:  # there are some fake prices that need to be removed, they're pure whitespace
                strippedExtractedPrices.append(strippedPrice)

        for link in extractedLinks:
            strippedLink = link.strip().strip('"') # we erase the whitespaces and the "" surrounding the name
            strippedExtractedLinks.append(strippedLink)
            if len(strippedLink) == 0:
                print("\n******A LINK WAS EMPTY!\n")

        try:
            # now that we cleaned the data, we can send it to the dataCollector
            collector.processNewData(currentRequestURL,
                                     strippedExtractedCars, strippedExtractedPrices, strippedExtractedLinks)
        except Exception:
            # print("An exception has happened. current round of collection failed.",
            #       "The traceback will be printed following this message.",
            #       "Collection rounds are going to continue despite failure.")
            # traceback.print_exc()
            logger.exception("Exception happened at Kijiji_Spyder")

        # print("Round Finished.")
        logger.info("Round finished")
