import scrapy
import psycopg2


class FindUtilInfo(scrapy.Spider):
    name = "utilityInfoScraper"

    connection = psycopg2.connect(
      dbname="postgres",
      user="postgres",
      password="pswd",
      host="127.0.0.1",
      port="5432"
    )
    connection.set_session(autocommit=True)

    print("UtilInfoScraper DB Connection status: " + str(connection.closed))  # should be zero if connection is open

    def start_requests(self):
        # with open("AllEWGUtilities.txt") as f:
        #     urls = f.read().splitlines()
        # for url in urls:
        yield scrapy.Request(url="https://www.ewg.org/tapwater/system.php?pws=MA4351000", callback=self.parse)

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

    def scrape_city_name(self, response):
        utility_name = response.meta["utility_name"]
        state_id = response.meta["state_id"]
        number_people_served = response.meta["number_people_served"]
        scraped_city = response.meta["scraped_city"]
        util_code = response.meta["util_code"]

        cursor = self.connection.cursor()
        cursor.execute("SELECT cities.id FROM cities WHERE cities.name = %s AND cities.state_id = %s",
                       (scraped_city, state_id))
        db_city = cursor.fetchone()

        # ("//ul[@class='contaminants-list']/li[section/div[@class='contaminant-name']"
        #  "/h3/text() = '{}']//div[@class='national-ppb-popup']/text()"
        #  .format(response.meta["cont_name"])).get()
        print("Aaaaaaaaaaaa {}".format(scraped_city))

        if not db_city:
            new_scraped_city = response.xpath("//tr[td/a[@href='system.php@pws={}']]/td[2]/text()".
                                              format(util_code)).get()
            cursor.execute("SELECT cities.id FROM cities WHERE cities.name = %s AND cities.state_id = %s",
                           (new_scraped_city, state_id))
            db_city = cursor.fetchone()

        cursor.execute("SELECT cities.county_id FROM cities WHERE cities.id = %s",
                       (db_city,))
        county = cursor.fetchone()

        # Check if the utility already exists
        cursor.execute("SELECT * FROM sources WHERE sources.utility_name = %s AND sources.state = %s",
                       (utility_name, state_id))
        result = cursor.fetchone()

        # if the utility does not exist, add it.
        if not result:
            cursor.execute("INSERT INTO sources (utility_name, city, county, state, number_served)"
                           " VALUES (%s, %s, %s, %s, %s)",
                           (utility_name, db_city, county, state_id, number_people_served))
        # Otherwise, update the data in it
        else:
            cursor.execute("UPDATE sources SET "
                           "utility_name=%s, city=%s, county = %s, state=%s, number_served=%s"
                           "WHERE source_id=%s",
                           (utility_name, db_city, county, state_id, number_people_served, result[0]))
        self.connection.commit()
        cursor.close()

    # this finds and writes all the info required for the sources table, and for the states table
    def scrape_source_info(self, response):
        try:
            util_code = response.url.split('=')[1]
            utility_name = response.xpath("//h1/text()").get()
            scraped_city = response.xpath("//ul[@class='served-ul']/li[1]/h2/text()").get().split(',')[0]
            if len(scraped_city.split(' ')) <= 1 or scraped_city.split(' ')[len(scraped_city.split(' '))-1] != 'County':

                state_id = util_code[0:2]
                number_people_served = int(response.xpath("//ul[@class='served-ul']/li[2]/h2/text()").get().split(' ')[1]
                                           .replace(',', ''))

                # https://www.ewg.org/tapwater/search-results.php?systemname=
                # West+Milford+Township+Municipal+Utilities+Authority+-+Birch+Hill+Park&stab=NJ&searchtype=systemname
                processed_city_name = scraped_city.replace(' ', '+')
                city_name_url = "https://www.ewg.org/tapwater/search-results.php?systemname={}&stab={}&" \
                                "searchtype=systemname".format(processed_city_name, state_id)
                yield scrapy.Request(url=city_name_url, callback=self.scrape_city_name, dont_filter=True, meta={
                    "utility_name": utility_name, "state_id": state_id, "number_people_served": number_people_served,
                    "scraped_city": scraped_city, "util_code": util_code})

        except Exception as e:
            with open('debugLog.txt', 'a') as f:
                f.write("ERROR: {}. Source Code: {}".format(e, response.url.split('=')[1]))
            print("ERROR: {}. Source Code: {}".format(e, response.url.split('=')[1]))

    def write_source_level(self, cont_name, src_id, this_utility_value):
        cursor = self.connection.cursor()

        # get the id of this contaminant based on its name
        cursor.execute("SELECT contaminant_id FROM contaminants WHERE contaminants.name = %s",
                       (cont_name,))
        cont_id = cursor.fetchone()

        # check if this source-contaminant relationship exists
        cursor.execute("SELECT * FROM source_levels WHERE source_levels.source_id = %s "
                       "AND source_levels.contaminant_id = %s", (src_id, cont_id))
        results = cursor.fetchall()

        # if there is not already a row for this contaminant-utility pair, add one,
        if not results:
            cursor.execute("INSERT INTO source_levels (source_id, contaminant_id, source_level)"
                           " VALUES (%s, %s, %s)", (src_id, cont_id, self.try_parse_float(this_utility_value)))
        # otherwise update the values
        else:
            cursor.execute("UPDATE source_levels SET source_level=%s WHERE source_id=%s AND contaminant_id=%s",
                           (self.try_parse_float(this_utility_value), src_id, cont_id))
        cursor.close()

    def write_state_avg(self, state_id, cont_name, state_avg):
        cursor = self.connection.cursor()

        # get the id of this contaminant based on its name
        cursor.execute("SELECT contaminant_id FROM contaminants WHERE contaminants.name = %s",
                       (cont_name,))
        cont_id = cursor.fetchone()

        # check if this state-contaminant relationship exists
        cursor.execute("SELECT * FROM state_avg_levels WHERE state_avg_levels.state_id = %s "
                       "AND state_avg_levels.contaminant_id = %s", (state_id, cont_id))
        results = cursor.fetchall()

        # if there is not already a row for this contaminant-state pair, add one,
        if not results:
            cursor.execute("INSERT INTO state_avg_levels (state_id, contaminant_id, state_avg)"
                           " VALUES (%s, %s, %s)", (state_id, cont_id, self.try_parse_float(state_avg)))
        # otherwise update the values
        else:
            cursor.execute("UPDATE state_avg_levels SET state_avg=%s WHERE state_id=%s AND contaminant_id=%s",
                           (self.try_parse_float(state_avg), state_id, cont_id))

        self.connection.commit()
        cursor.close()

    def scrape_source_levels(self, response):
        cont_raw = response.xpath("//ul[@class='contaminants-list']/li/section[contains(@class, 'contaminant-data')]")
        source_name = response.xpath("//h1/text()").get()
        source_state = response.url.split('=')[1][0:2]

        cursor = self.connection.cursor()
        cursor.execute("SELECT source_id FROM sources WHERE sources.utility_name = %s AND sources.state = %s",
                       (source_name, source_state))
        src_id = cursor.fetchone()
        cursor.close()

        for cont in cont_raw:
            try:
                # If the description for measured contaminants exists
                if cont.xpath(".//div[@class='this-utility-ppb-popup']/text()").get() is not None:
                    cont_name = cont.xpath(".//div[@class='contaminant-name']/h3/text()").get()

                    this_utility_value = \
                        cont.xpath(".//div[@class='this-utility-ppb-popup']/text()").get().split(' ')[0]
                    state_avg = cont.xpath(".//div[@class='state-ppb-popup']/text()").get().split(' ')[0]

                    self.write_source_level(cont_name, src_id, this_utility_value)
                    self.write_state_avg(source_state, cont_name, state_avg)

                # If the description for non-measured (only detected) contaminants exists
                elif cont.xpath(".//div[@class = 'slide-toggle']/p[1]/a[1]/text()").get() is not None:
                    cont_name = cont.xpath(".//div[@class = 'slide-toggle']/p[1]/a[1]/text()").get()

                    this_utility_value = None
                    state_avg = None
                    self.write_source_level(cont_name, src_id, this_utility_value)
                    self.write_state_avg(source_state, cont_name, state_avg)

            except Exception as e:
                with open('debugLog.txt', 'a') as f:
                    f.write("ERROR: {}. Source Name: {}, State: {}".format(e, source_name, source_state))
                print("ERROR: {}. Source Name: {}, State: {}".format(e, source_name, source_state))
        self.connection.commit()

    def parse(self, response):
        try:
            self.scrape_source_info(response)
            self.scrape_source_levels(response)

        except Exception as e:
            print("Error in parse, {}".format(e))
