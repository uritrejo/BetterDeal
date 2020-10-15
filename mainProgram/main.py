from twisted.internet import reactor, task
from dataExtraction.dataExtraction.spiders.kijiji_spider import KijijiSpider
import database
from notification.notification_manager import *
from scrapy.crawler import CrawlerRunner

def run_spider():

    print("Creo que tengo que borrar este, pero por algo lo he de haber puesto bro")

    # Run a spider within Twisted every X seconds

    # print("run_spider")

    # runner = CrawlerRunner()
    # runner.crawl(KijijiSpider)

    # print("Pony")
    #
    # database.retrieveCars()


    # deferred = task.deferLater(reactor, 10, run_spider)

    # this didn't work, but it might come in handy later: deferred.addCallback(reactor.callLater, 5, run_spider) #attempt 1

    # return deferred


print("Starting process...")
run_spider()
reactor.run()   # you have to run the reactor yourself