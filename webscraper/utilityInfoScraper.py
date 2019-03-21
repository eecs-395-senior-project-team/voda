#!/usr/bin/env python3

import scrapy
import psycopg2


class FindInfo(scrapy.Spider):
    name = "utilityInfoScraper"

    connection = psycopg2.connect(
      dbname="postgres",
      user="postgres",
      password="pswd",
      host="127.0.0.1",
      port="5432"
    )
    connection.set_session(autocommit=True)

    print("Connection status: " + str(connection.closed))  # should be zero if connection is open

    def start_requests(self):
        with open("./resultFiles/AllEWGUtilities.txt") as f:
            urls = f.read().splitlines()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        #  url = "https://www.ewg.org/tapwater/system.php?pws=OH1800403"
        # yield scrapy.Request(url=url, callback=self.parse)

    @staticmethod
    def try_parse_float(float_to_be_parsed):
        try:
            if float_to_be_parsed is None:
                return None
            else:
                return float(float_to_be_parsed.replace(',', ''))
        except Exception:
            return float(float_to_be_parsed)

    # this finds and writes all the info required for the sources table, and for the states table
    def scrape_source_info(self, response):
        try:
            util_code = response.url.split('=')[1]
            utility_name = response.xpath("//h1/text()").get()
            city = response.xpath("//ul[@class='served-ul']/li[1]/h2/text()").get().split(',')[0]
            state_id = util_code[0:2]
            number_people_served = int(response.xpath("//ul[@class='served-ul']/li[2]/h2/text()").get().split(' ')[1]
                                       .replace(',', ''))

            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM states WHERE states.state_id = (%s)", (state_id, ))
            result = cursor.fetchone()
            # if the state is not already in the table, add it
            if not result:
                cursor.execute("INSERT INTO states (state_id) VALUES (%s)", (state_id, ))

            cursor.execute("SELECT * FROM sources WHERE sources.utility_name = (%s)", (utility_name, ))
            result = cursor.fetchone()
            # if the utility does not exist, add it.
            if not result:
                cursor.execute("INSERT INTO sources (utility_name, city, state, number_served)"
                               " VALUES (%s, %s, %s, %s)", (utility_name, city, state_id, number_people_served))
            # Otherwise, update the data in it
            else:
                cursor.execute("UPDATE sources SET "
                               "utility_name=(%s), city=(%s), state=(%s), number_served=(%s)"
                               "WHERE source_id=(%s)",
                               (utility_name, city, state_id, number_people_served, result[0]))
            self.connection.commit()
            cursor.close()
        except Exception as e:
            with open('./debugLog.txt', 'a') as f:
                f.write("ERROR: {}".format(e))
            print(e)

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
        cont_above_gl_raw = response.xpath("//ul[@id='contams_above_hbl']/li/section[@class='contaminant-data']")
        source_name = response.xpath("//h1/text()").get()
        source_state = response.url.split('=')[1][0:2]

        cursor = self.connection.cursor()
        cursor.execute("SELECT source_id FROM sources WHERE sources.utility_name = %s AND sources.state = %s",
                       (source_name, source_state))
        src_id = cursor.fetchone()
        cursor.close()

        for cont in cont_above_gl_raw:
            try:
                # If the description for measured contaminants exists
                if cont.xpath(".//div[@class='health-guideline-ppb']/text()").get() is not None:
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
                with open('./debugLog.txt', 'a') as f:
                    f.write("ERROR: {}".format(e))
                print(e)
        self.connection.commit()

    def parse(self, response):
        try:
            self.scrape_source_info(response)
            self.scrape_source_levels(response)
            # print(response.url)

            #  nameOfProvider = response.xpath("//h1/text()").get()
            # city = response.xpath("//ul[@class='served-ul']/li[1]/h2/text()").get()
            # numberPeopleServed = response.xpath("//ul[@class='served-ul']/li[2]/h2/text()").get().split(' ')[1]
            # state = utilCode[0:2]
            # write to the db
            # cursor.execute("SELECT * FROM sources WHERE sources.source_id = %s", [utilCode])
            # results = cursor.fetchall()
            # if not results:
            #     cursor.execute("INSERT INTO sources (city, source_id, name, state) VALUES (%s, %s, %s, %s)",
            #                (city, utilCode, nameOfProvider, state))
            # self.connection.commit()
            # cursor.close()

            # cursor = self.connection.cursor()
            # contAboveGLRaw = response.xpath("//ul[@id='contams_above_hbl']/li/section[@class='contaminant-data']")
            # contAboveGL = ""
            # for cont in contAboveGLRaw:
            #     if cont.xpath(".//div[@class='health-guideline-ppb']/text()").get() is not None:
            #         contAboveGL += "\n" + cont.xpath("./div[1]/h3/text()").get() + ",\n" +\
            #            "HEALTH_GL: " + cont.xpath(".//div[@class='health-guideline-ppb']/text()").extract()[1]
            #            + ",\n"+\
            #            "NATIONAL_AVG: " + cont.xpath(".//div[@class='national-ppb-popup']/text()").get() + ",\n" +\
            #            "STATE_AVG: " + cont.xpath(".//div[@class='state-ppb-popup']/text()").get() + ",\n" +\
            #            "THIS_UTIL: " + cont.xpath(".//div[@class='this-utility-ppb-popup']/text()").get() + ";"
            #         healthGL = cont.xpath(".//div[@class='health-guideline-ppb']/text()").extract()[1]
            #         natAvg = cont.xpath(".//div[@class='national-ppb-popup']/text()").get()
            #         thisUtil = cont.xpath(".//div[@class='this-utility-ppb-popup']/text()").get()
            #         contName = cont.xpath("./div[1]/h3/text()").get()
            #
            #         cursor.execute("SELECT contaminant_id FROM contaminants"
            #                                     " WHERE contaminants.name='{}'".format(contName))
            #         results = cursor.fetchall()
            #
            #         if not results:
            #             cursor.execute("INSERT INTO contaminants (name, health_guideline, national_average) VALUES"
            #                            " (%s, %s, %s)", (contName, healthGL, natAvg))
            #             self.connection.commit()
            #             cursor.close()
            #         cursor = self.connection.cursor()
            #         # cursor.execute("UPDATE source_levels SET contaminant_id=%s, source_id=%s, contaminant_level=%s"
            #         #                , [results[0], utilCode, thisUtil])
            #
            #     elif cont.xpath(".//div[@class = 'slide-toggle']/p[1]/a[1]/text()").get() is not None:
            #         contAboveGL += "\n" + cont.xpath("./div[1]/h3/text()").get() + ",\n"\
            #            "RADIATION_DETECTED: " + cont.xpath(".//div[@class = 'slide-toggle']
            #            /p[1]/a[1]/text()").get()+";"
            #         thisUtil = cont.xpath(".//div[@class = 'slide-toggle']/p[1]/a[1]/text()").get()
            #         contName = cont.xpath("./div[1]/h3/text()").get()
            #
            # self.connection.commit()
            # cursor.close()
            #
            # otherContDetRaw = response.xpath("//ul[@id='contams_other']/li/section[@class='contaminant-data']")
            # otherContDet = ""
            # for cont in otherContDetRaw:
            #     if cont.xpath(".//div[@class='this-utility-ppb-popup']/text()").get() is not None:
            #         otherContDet += "\n" + cont.xpath("./div[1]/h3/text()").get() + ",\n"\
            #            "NATIONAL_AVG: " + cont.xpath(".//div[@class='national-ppb-popup']/text()").get() + ",\n" +\
            #            "STATE_AVG: " + cont.xpath(".//div[@class='state-ppb-popup']/text()").get() + ",\n" +\
            #            "THIS_UTIL: " + cont.xpath(".//div[@class='this-utility-ppb-popup']/text()").get() + ";"
            #
            # otherContNotDet=""
            # otherContNotDetRaw = response.xpath("//section[@class='contams-not-detected']
            # /div[2]/p[2]/a/text()").getall()
            # for cont in otherContNotDetRaw:
            #     otherContNotDet += "\n" + cont + ";"
            #
            # info = "{{{};{};{};{}\n\n" \
            #        "CONT_ABOVE_GL:({})\n\n" \
            #        "OTHER_CONT_DETECTED:({})\n\n" \
            #        "OTHER_NOT_DETECTED:({})}}\n\n".format\
            #     (utilCode, nameOfProvider, city, numberPeopleServed, contAboveGL, otherContDet, otherContNotDet)
            #
            #
            #
            # self.connection.close()
            # with open('./resultFiles/FinalInfoTest.txt', 'a') as f:
            #     f.write(info)

        except Exception as e:
            # with open('./resultFiles/FinalInfoTest.txt', 'a') as f:
            #     f.write("ERROR: {}".format(e))
            print(e)
