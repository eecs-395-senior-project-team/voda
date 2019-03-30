from getContaminantsScraper import FindContaminants
from contaminantInfoScraper import FindContInfo
from findUtilitiesScraper import FindUtilities
from utilityInfoScraper import FindUtilInfo
from calculateSourceRating import CalculateSourceRating
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner


if __name__ == '__main__':
    runner = CrawlerRunner()

    @defer.inlineCallbacks
    def crawl():
        print("Beginning FindContaminants Spider")
        yield runner.crawl(FindContaminants)
        print("Ending FindContaminants Spider")

        print("Beginning FindContInfo Spider")
        yield runner.crawl(FindContInfo)
        print("Ending FindContInfo Spider")

        print("Beginning FindUtilities Spider")
        yield runner.crawl(FindUtilities)
        print("Ending FindUtilities Spider")

        print("Beginning FindUtilInfo Spider")
        yield runner.crawl(FindUtilInfo)
        print("Ending FindUtilInfo Spider")

        reactor.stop()

    crawl()
    reactor.run()  # script will block here until all crawlers are finished
    calculateSourceRating = CalculateSourceRating()
    calculateSourceRating.main()
