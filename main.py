from twisted.internet import reactor, task
from dataExtraction.dataExtraction.spiders.kijiji_spider import KijijiSpider
from notification.notification_manager import *
from scrapy.crawler import CrawlerRunner
import dataExtraction.dataCollector as collector


def run_spider():

    # Run a spider within Twisted every X seconds
    print("run_spider")
    print("Current amount of cars: ", len(collector.cars))

    runner = CrawlerRunner()
    runner.crawl(KijijiSpider)

    deferred = task.deferLater(reactor, config.TIME_BETWEEN_ROUNDS, run_spider)

    return deferred


print("Starting process...")
run_spider()
reactor.run()

# sendEmailNotification("A good car", "$420", "link.com")
