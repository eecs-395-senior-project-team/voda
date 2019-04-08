from vodaData.getContaminantsScraper import FindContaminants
from vodaData.contaminantInfoScraper import FindContInfo
from vodaData.findUtilitiesScraper import FindUtilities
from vodaData.utilityInfoScraper import FindUtilInfo
from vodaData.sourceLevelScraper import FindSourceLevels
from vodaData.calculateSourceRating import CalculateSourceRating
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from vodaData.getLocaleData import GetLocaleData


if __name__ == '__main__':
    runner = CrawlerRunner()

    @defer.inlineCallbacks
    def crawl():
        print("Beginning FindContaminants Spider")
        with open('./vodaData/debugLog.txt', 'a') as f:
            f.write("Beginning FindContaminants Spider\n")
        yield runner.crawl(FindContaminants)
        with open('./vodaData/debugLog.txt', 'a') as f:
            f.write("Ending FindContaminants Spider\n")
        print("Ending FindContaminants Spider")

        with open('./vodaData/debugLog.txt', 'a') as f:
            f.write("Beginning FindContInfo Spider\n")
        print("Beginning FindContInfo Spider")
        yield runner.crawl(FindContInfo)
        with open('./vodaData/debugLog.txt', 'a') as f:
            f.write("Ending FindContInfo Spider\n")
        print("Ending FindContInfo Spider")

        print("Beginning FindUtilities Spider")
        with open('./vodaData/debugLog.txt', 'a') as f:
            f.write("Beginning FindUtilities Spider\n")
        yield runner.crawl(FindUtilities)
        with open('./vodaData/debugLog.txt', 'a') as f:
            f.write("Ending FindUtilities \n")
        print("Ending FindUtilities Spider")

        print("Beginning FindUtilInfo Spider")
        with open('./vodaData/debugLog.txt', 'a') as f:
            f.write("Beginning FindUtilInfo Spider\n")
        yield runner.crawl(FindUtilInfo)
        with open('./vodaData/debugLog.txt', 'a') as f:
            f.write("Ending FindUtilInfo Spider\n")
        print("Ending FindUtilInfo Spider")

        print("Beginning FindSourceLevels Spider")
        with open('./vodaData/debugLog.txt', 'a') as f:
            f.write("Beginning FindSourceLevels Spider\n")
        yield runner.crawl(FindSourceLevels)
        with open('./vodaData/debugLog.txt', 'a') as f:
            f.write("Ending FindSourceLevels Spider\n")
        print("Ending FindSourceLevels Spider")

        reactor.stop()

    print("Beginning GetLocaleData")
    with open('./vodaData/debugLog.txt', 'a') as f:
        f.write("Beginning GetLocaleData Spider")
    get_locale_data = GetLocaleData()
    get_locale_data.main()
    with open('./vodaData/debugLog.txt', 'a') as f:
        f.write("Ending GetLocaleData Spider")
    print("Ending GetLocaleData")

    crawl()
    reactor.run()  # script will block here until all crawlers are finished

    print("Beginning CalculateSourceRating")
    with open('./vodaData/debugLog.txt', 'a') as f:
        f.write("Beginning CalculateSourceRating Spider")
    calculate_source_rating = CalculateSourceRating()
    calculate_source_rating.main()
    with open('./vodaData/debugLog.txt', 'a') as f:
        f.write("Ending CalculateSourceRating Spider")
    print("Ending CalculateSourceRating")

