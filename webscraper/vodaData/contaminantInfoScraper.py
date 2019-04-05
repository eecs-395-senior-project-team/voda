import scrapy
import psycopg2


class FindContInfo(scrapy.Spider):
    name = "utilityInfoScraper"

    open('./vodaData/debugLog.txt', "w").close()

    connection = psycopg2.connect(
      dbname="postgres",
      user="postgres",
      password="pswd",
      host="127.0.0.1",
      port="5432"
    )
    # should be zero if connection is open
    print("ContaminantInfoScraper DB Connection status: " + str(connection.closed))

    def start_requests(self):
        with open("./vodaData/AllContaminants.txt") as f:
            urls = f.read().splitlines()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    @staticmethod
    def try_parse_float(float_to_be_parsed):
        if float_to_be_parsed is None:
            return None
        elif float_to_be_parsed == 'ND':
            return 0.0
        elif type(float_to_be_parsed) == str:
            return float(float_to_be_parsed.replace(',', ''))
        else:
            return float(float_to_be_parsed)

    def second_level_parse(self, response):
        try:
            try_nat_avg = response.xpath("//ul[@class='contaminants-list']/li[section/div[@class='contaminant-name']"
                                         "/h3/text() = '{}']//div[@class='national-ppb-popup']/text()"
                                         .format(response.meta["cont_name"])).get()
            if try_nat_avg is not None:
                national_avg = try_nat_avg.split(' ')[0]
            else:
                national_avg = None

            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM contaminants WHERE contaminants.name = (%s)", (response.meta["cont_name"], ))
            result = cursor.fetchone()

            if not result:
                cursor.execute("INSERT INTO contaminants "
                               "(name, legal_limit, national_avg, summary, health_concerns,"
                               " long_health_concerns, health_guideline)"
                               " VALUES (%s, %s, %s, %s, %s, %s, %s)",
                               (response.meta["cont_name"], self.try_parse_float(response.meta["legal_limit"]),
                                self.try_parse_float(national_avg), response.meta["summary"],
                                response.meta["health_concerns"], response.meta["long_concerns"],
                                self.try_parse_float(response.meta["health_guideline"])))
            else:
                cursor.execute("UPDATE contaminants SET "
                               "name=(%s), legal_limit=(%s), national_avg=(%s), summary=(%s),"
                               "health_concerns=(%s), long_health_concerns=(%s), health_guideline=(%s)"
                               "WHERE contaminant_id=(%s)",
                               (response.meta["cont_name"], self.try_parse_float(response.meta["legal_limit"]),
                                self.try_parse_float(national_avg), response.meta["summary"],
                                response.meta["health_concerns"], response.meta["long_concerns"],
                                self.try_parse_float(response.meta["health_guideline"]),
                                result[0]))
            self.connection.commit()
            cursor.close()
        except Exception as e:
            with open('./vodaData/debugLog.txt', 'a') as f:
                f.write("Second level ERROR: {}".format(e))
            print(e)

    def parse(self, response):
        try:
            with open('./vodaData/test.txt', 'a') as f:
                f.write("contaminantInfoScraper\n")
            health_concerns = ""

            cont_name = response.xpath("//h1/text()").get()

            try_legal_limit = response.xpath("//section[@class='drinking-water-standards']/p[3]/span/text()").get()
            if try_legal_limit is not None:
                legal_limit = try_legal_limit.split(' ')[0]
            else:
                legal_limit = None

            summary = response.xpath("//div[@class='contamdesc-wrapper']/p[1]/text()").get()

            health_concerns_arr = response.xpath("//section[@class='health-concerns']/p/text()").getall()
            for concern in health_concerns_arr:
                health_concerns += (concern + '\n')

            long_concerns = response.xpath("//div[@class='contamdesc-wrapper']/p[2]/text()").get()
            try_health_guideline = response.xpath(
                "//section[@class='drinking-water-standards']/p[1]/span/text()").get()

            if try_health_guideline is not None:
                health_guideline = try_health_guideline.split(' ')[0]
            else:
                health_guideline = None

            # get the url for a source guaranteed to have this contaminant
            national_avg_source = "https://www.ewg.org/tapwater/" + \
                                  response.xpath("//table""[@class='community-contaminant-table']"
                                                 "/tbody/tr/td[@data-label='Utility']/a[text()!='']/@href").get()

            yield scrapy.Request(url=national_avg_source, callback=self.second_level_parse, dont_filter=True, meta={
                "cont_name": cont_name, "legal_limit": legal_limit, "summary": summary,
                "health_concerns": health_concerns, "long_concerns": long_concerns,
                "health_guideline": health_guideline})

        except Exception as e:
            with open('./vodaData/debugLog.txt', 'a') as f:
                f.write("First level ERROR: {}".format(e))
            print(e)
