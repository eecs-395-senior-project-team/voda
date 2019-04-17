import scrapy
import psycopg2


class FindSourceLevels(scrapy.Spider):
    name = "sourceLevelScraper"

    def __init__(self, connection):
        self.connection = connection

    def start_requests(self):
        with open("./vodadata/AllEWGUtilities.txt") as f:
            urls = f.read().splitlines()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.scrape_source_levels)

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
        try:
            cont_raw = response.xpath(
                "//ul[@class='contaminants-list']/li/section[contains(@class, 'contaminant-data')]")
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
                        f.write("\nERROR: {}. Source Name: {}, State: {}".format(e, source_name, source_state))
                    print("ERROR: {}. Source Name: {}, State: {}".format(e, source_name, source_state))
            self.connection.commit()

        except Exception as e:
            print(e)
