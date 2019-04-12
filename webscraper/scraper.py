from vodadata.getContaminantsScraper import FindContaminants
from vodadata.contaminantInfoScraper import FindContInfo
from vodadata.findUtilitiesScraper import FindUtilities
from vodadata.utilityInfoScraper import FindUtilInfo
from vodadata.sourceLevelScraper import FindSourceLevels
from vodadata.calculateSourceRating import CalculateSourceRating
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from vodadata.getLocaleData import GetLocaleData


if __name__ == '__main__':
    RUNNER = CrawlerRunner()

    @defer.inlineCallbacks
    def crawl():
        print("Beginning FindContaminants Spider")
        with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
            f.write("Beginning FindContaminants Spider\n")
        yield RUNNER.crawl(FindContaminants)
        with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
            f.write("Ending FindContaminants Spider\n")
        print("Ending FindContaminants Spider")

        with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
            f.write("Beginning FindContInfo Spider\n")
        print("Beginning FindContInfo Spider")
        yield RUNNER.crawl(FindContInfo)
        with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
            f.write("Ending FindContInfo Spider\n")
        print("Ending FindContInfo Spider")

        print("Beginning FindUtilities Spider")
        with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
            f.write("Beginning FindUtilities Spider\n")
        yield RUNNER.crawl(FindUtilities)
        with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
            f.write("Ending FindUtilities \n")
        print("Ending FindUtilities Spider")

        print("Beginning FindUtilInfo Spider")
        with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
            f.write("Beginning FindUtilInfo Spider\n")
        yield RUNNER.crawl(FindUtilInfo)
        with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
            f.write("Ending FindUtilInfo Spider\n")
        print("Ending FindUtilInfo Spider")

        print("Beginning FindSourceLevels Spider")
        with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
            f.write("Beginning FindSourceLevels Spider\n")
        yield RUNNER.crawl(FindSourceLevels)
        with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
            f.write("Ending FindSourceLevels Spider\n")
        print("Ending FindSourceLevels Spider")

        reactor.stop()

    print("Beginning GetLocaleData")
    with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
        f.write("Beginning GetLocaleData Spider")
    get_locale_data = GetLocaleData()
    get_locale_data.main()
    with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
        f.write("Ending GetLocaleData Spider")
    print("Ending GetLocaleData")

    crawl()
    reactor.run()  # script will block here until all crawlers are finished

    print("Beginning CalculateSourceRating")
    with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
        f.write("Beginning CalculateSourceRating Spider")
    calculate_source_rating = CalculateSourceRating()
    calculate_source_rating.main()
    with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
        f.write("Ending CalculateSourceRating Spider")
    print("Ending CalculateSourceRating")
