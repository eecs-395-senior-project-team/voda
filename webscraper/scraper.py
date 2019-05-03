from vodadata.getContaminantsScraper import FindContaminants
from vodadata.contaminantInfoScraper import FindContInfo
from vodadata.findUtilitiesScraper import FindUtilities
from vodadata.utilityInfoScraper import FindUtilInfo
from vodadata.sourceLevelScraper import FindSourceLevels
from vodadata.calculateSourceRating import CalculateSourceRating
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from vodadata.getLocaleData import GetLocaleData
from vodadata.leadInfoScraper import LeadInfoScraper
import psycopg2
import os
import traceback


if __name__ == '__main__':
    RUNNER = CrawlerRunner()

    DBNAME = os.environ['POSTGRES_DB']
    USER = os.environ['POSTGRES_USER']
    PASSWORD = os.environ['POSTGRES_PASSWORD']
    HOST = os.environ['POSTGRES_HOST']
    PORT = os.environ['POSTGRES_PORT']

    CONNECTION = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
    CONNECTION.set_session(autocommit=True)

    print("DB Connection status: " + str(CONNECTION.closed))  # should be zero if connection is open

    def clearData():
        print("Started Wiping Database")
        with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
            f.write("Started Wiping Database\n")
        try:
            cursor = CONNECTION.cursor()
            cursor.execute('DELETE FROM "vodaMainApp_sourcelevels"') 
            cursor.execute('DELETE FROM "vodaMainApp_stateavglevels"')
            cursor.execute('DELETE FROM "vodaMainApp_sources"')
            cursor.execute('DELETE FROM "vodaMainApp_contaminants"')
            cursor.execute('DELETE FROM "vodaMainApp_cities"')
            cursor.execute('DELETE FROM "vodaMainApp_counties"')
            cursor.execute('DELETE FROM "vodaMainApp_states"') 
            cursor.close()
        except Exception as e: 
            print('ERROR\n{}'.format(traceback.format_exc()))
            with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
                f.write("Error wiping database:\n{}\n".format(e))

        print("Finished Wiping Database")
        with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
            f.write("Finished Wiping Database\n")
        
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
        yield RUNNER.crawl(FindContInfo, CONNECTION)
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
        yield RUNNER.crawl(FindUtilInfo, CONNECTION)
        with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
            f.write("Ending FindUtilInfo Spider\n")
        print("Ending FindUtilInfo Spider")

        print("Beginning FindSourceLevels Spider")
        with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
            f.write("Beginning FindSourceLevels Spider\n")
        yield RUNNER.crawl(FindSourceLevels, CONNECTION)
        with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
            f.write("Ending FindSourceLevels Spider\n")
        print("Ending FindSourceLevels Spider")

        print("Beginning LeadInfoScraper Spider")
        with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
            f.write("Beginning LeadInfoScraper Spider\n")
        yield RUNNER.crawl(LeadInfoScraper, CONNECTION)
        with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
            f.write("Ending LeadInfoScraper Spider\n")
        print("Ending LeadInfoScraper Spider")

        reactor.stop()

    #### main execution section ####
    clearData()

    print("Beginning GetLocaleData")
    with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
        f.write("Beginning GetLocaleData Spider\n")
    get_locale_data = GetLocaleData(CONNECTION)
    get_locale_data.main()
    with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
        f.write("Ending GetLocaleData Spider\n")
    print("Ending GetLocaleData")

    crawl()
    reactor.run()  # script will block here until all crawlers are finished

    print("Beginning CalculateSourceRating")
    with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
        f.write("Beginning CalculateSourceRating Spider\n")
    calculate_source_rating = CalculateSourceRating(CONNECTION)
    calculate_source_rating.main()
    with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
        f.write("Ending CalculateSourceRating Spider\n")
    print("Ending CalculateSourceRating")
