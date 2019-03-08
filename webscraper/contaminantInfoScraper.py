import scrapy
import psycopg2
from psycopg2 import sql


class FindInfo(scrapy.Spider):
    name = "utilityInfoScraper"
    national_avg = None
    cont_name = None
    legal_limit = None
    summary = None
    health_concern = None
    long_concerns = None
    health_guideline = None


    connection = psycopg2.connect(
      dbname="postgres",
      user="postgres",
      password="pswd",
      host="127.0.0.1",
      port="5432"
    )
    print("Connection status: " + str(connection.closed))  # should be zero if connection is open

    def start_requests(self):
        with open("./resultFiles/AllContaminants.txt") as f:
            urls = f.read().splitlines()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
      # url = "https://www.ewg.org/tapwater/contaminant.php?contamcode=2980#"
      # yield scrapy.Request(url=url, callback=self.parse)

    def tryParseFloat(self, floatToBeParsed):
        try:
            if floatToBeParsed is None:
                return None
            else:
                return float(floatToBeParsed.replace(',',''))
        except:
            float(floatToBeParsed)

    def try_nat_average(self, try_nat_avg):
        if try_nat_avg == 'ND':
            return None
        else:
            return try_nat_avg

    def second_level_parse(self, response):
        try:
            try_nat_avg = response.xpath("//ul[@class='contaminants-list']/li[section/div[@class='contaminant-name']"
                                               "/h3/text() = '{}']//div[@class='national-ppb-popup']/text()"
                                               .format(self.cont_name)).get()
            if try_nat_avg is not None:
                self.national_avg = try_nat_avg.split(' ')[0]
            else:
                self.national_avg = None

            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM contaminants WHERE contaminants.name = (%s)", (self.cont_name, ))
            result = cursor.fetchone()
            if not result:
                print("insert: " + self.cont_name)
                cursor.execute("INSERT INTO contaminants "
                               "(name, legal_limit, national_avg, summary, health_concerns,"
                               " long_health_concerns, health_guideline)"
                           " VALUES (%s, %s, %s, %s, %s, %s, %s)",
                               (self.cont_name, self.tryParseFloat(self.legal_limit),
                                self.tryParseFloat(self.national_avg), self.summary,
                                self.health_concerns, self.long_concerns, self.tryParseFloat(self.health_guideline)))
            else:
                print("update: " + self.cont_name)
                cursor.execute("UPDATE contaminants SET "
                               "name=(%s), legal_limit=(%s), national_avg=(%s), summary=(%s),"
                               "health_concerns=(%s), long_health_concerns=(%s), health_guideline=(%s)"
                               "WHERE contaminant_id=(%s)",
                               (self.cont_name, self.tryParseFloat(self.legal_limit),
                                self.tryParseFloat(self.national_avg), self.summary,
                                self.health_concerns, self.long_concerns, self.tryParseFloat(self.health_guideline),
                                result[0]))
            self.connection.commit()
            cursor.close()
        except Exception as e:
            with open('./debugLog.txt', 'a') as f:
                f.write("ERROR: {}".format(e))
            print(e)

    def parse(self, response):
        try:
            self.health_concerns = ""

            self.cont_name = response.xpath("//h1/text()").get()

            try_legal_limit = response.xpath("//section[@class='drinking-water-standards']/p[3]/span/text()").get()
            if try_legal_limit is not None:
                self.legal_limit = try_legal_limit.split(' ')[0]
            else:
                self.legal_limit = None

            self.summary = response.xpath("//div[@class='contamdesc-wrapper']/p[1]/text()").get()

            health_concerns_arr = response.xpath("//section[@class='health-concerns']/p/text()").getall()
            health_concerns = ""
            for concern in health_concerns_arr:
                self.health_concerns += (concern + '\n')

            self.long_concerns = response.xpath("//div[@class='contamdesc-wrapper']/p[2]/text()").get()
            try_health_guideline = response.xpath(
                "//section[@class='drinking-water-standards']/p[1]/span/text()").get()

            if try_health_guideline is not None:
                self.health_guideline = try_health_guideline.split(' ')[0]
            else:
                self.health_guideline = None

            self.national_avg_source = "https://www.ewg.org/tapwater/" + \
                                       response.xpath("//table""[@class='community-contaminant-table']"
                                                      "/tbody/tr[1]/td[@data-label='Utility']/a/@href").get()
            yield scrapy.Request(url=self.national_avg_source, callback=self.second_level_parse,)

        except Exception as e:
            with open('./debugLog.txt', 'a') as f:
                 f.write("ERROR: {}".format(e))
            print(e)
