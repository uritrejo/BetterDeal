from twisted.internet import reactor, task
from dataExtraction.dataExtraction.spiders.kijiji_spider import KijijiSpider
from notification.notification_manager import *
from scrapy.crawler import CrawlerRunner
import notification.email_config
import dataExtraction.dataCollector
import database.database as db

def run_spider():

    # Run a spider within Twisted every X seconds
    print("run_spider")
    print("Current amount of cars: ", len(dataExtraction.dataCollector.cars))
    # KijijiSpider.start_urls = db.retrieveSearches()

    # print(KijijiSpider.start_urls)
    runner = CrawlerRunner()
    runner.crawl(KijijiSpider)

    deferred = task.deferLater(reactor, config.TIME_BETWEEN_ROUNDS, run_spider)

    return deferred


print("Starting process...")
run_spider()
reactor.run()