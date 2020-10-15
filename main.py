from twisted.internet import reactor, task
from dataExtraction.dataExtraction.spiders.kijiji_spider import KijijiSpider
from notification.notification_manager import *
from scrapy.crawler import CrawlerRunner
import notification.email_config
import dataExtraction.dataCollector
import database.database

def run_spider():

    # Run a spider within Twisted every X seconds

    # print("run_spider")

    # print("Current amount of cars: ", len(dataExtraction.dataCollector.cars))
    #
    #
    # runner = CrawlerRunner()
    # runner.crawl(KijijiSpider)

    print("Pony")

    database.database.retrieveCars()

    # this didn't work, but it might come in handy later: deferred.addCallback(reactor.callLater, 5, run_spider) #attempt 1
    deferred = task.deferLater(reactor, config.TIME_BETWEEN_ROUNDS, run_spider)

    return deferred


print("Starting process...")
run_spider()
reactor.run()   # you have to run the reactor yourself