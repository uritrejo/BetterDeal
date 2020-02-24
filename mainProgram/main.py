from twisted.internet import reactor
from dataExtraction.dataExtraction.spiders.kijiji_spider import KijijiSpider
from scrapy.crawler import CrawlerRunner

def run_spider():

    # Run a spider within Twisted every 20 seconds

    print("run_spider")

    runner = CrawlerRunner()
    deferred = runner.crawl(KijijiSpider)
    # you can use reactor.callLater or task.deferLater to schedule a function
    deferred.addCallback(reactor.callLater, 20, run_spider)
    return deferred


print("Starting process...")
run_spider()
reactor.run()   # you have to run the reactor yourself