import scrapy
import psycopg2


class FindUtilInfo(scrapy.Spider):
    counter = 0
    name = "utilityInfoScraper"

    def __init__(self, connection):
        self.connection = connection

    def start_requests(self):
        with open("./vodadata/datafiles/AllEWGUtilities.txt") as f:
            urls = f.read().splitlines()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.scrape_source_info)

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
        try: 
            utility_name = response.meta["utility_name"]
            state_id = response.meta["state_id"]
            number_people_served = response.meta["number_people_served"]
            scraped_city = response.meta["scraped_city"]
            util_code = response.meta["util_code"]
            url = response.meta["url"]

            cursor = self.connection.cursor()
            cursor.execute('SELECT id FROM "vodaMainApp_cities" WHERE name = %s AND state_id = %s',
                           (scraped_city, state_id))
            db_city = cursor.fetchone()

            if not db_city:
                new_scraped_city = response.xpath("//tr[td/a[@href='system.php?pws={}']]/td[2]/text()".
                                                  format(util_code)).get()
                cursor.execute('SELECT id FROM "vodaMainApp_cities" WHERE name = %s AND state_id = %s',
                               (new_scraped_city, state_id))
                db_city = cursor.fetchone()
                if db_city is None:
                    reduced_scraped_city = None
                    if len(new_scraped_city.split(' ')) > 1:
                        reduced_scraped_city = ' '.join(scraped_city.split(' ')[0: len(scraped_city.split(' '))-1])

                        cursor.execute('SELECT id FROM "vodaMainApp_cities" WHERE name = %s AND state_id = %s',
                                       (reduced_scraped_city, state_id))
                        db_city = cursor.fetchone()

                    if db_city is None:
                        self.counter = self.counter + 1
                        with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
                            f.write("\nCounter: {}\nCity could not be found:{}, {}, {}, {}, {}, {}, {}\n People Served:{}\n".format(self.counter, response.url,utility_name,scraped_city,new_scraped_city,reduced_scraped_city, state_id,util_code, number_people_served))

            cursor.execute('SELECT county_id FROM "vodaMainApp_cities" WHERE id = %s',
                           (db_city,))
            county = cursor.fetchone()

            # Check if the utility already exists
            cursor.execute('SELECT * FROM "vodaMainApp_sources" WHERE utility_name = %s AND state_id = %s',
                           (utility_name, state_id))
            result = cursor.fetchone()
    
            #if we could not match the city we do not want to try to add it
            if db_city is None:
                pass

            # if the utility does not exist, add it.
            elif not result:
                cursor.execute('INSERT INTO "vodaMainApp_sources" (utility_name, city_id, county_id, state_id, number_served, url)'
                               ' VALUES (%s, %s, %s, %s, %s, %s)',
                               (utility_name, db_city, county, state_id, number_people_served, url))
            # Otherwise, update the data in it
            else:
                cursor.execute('UPDATE "vodaMainApp_sources" SET '
                               'utility_name=%s, city_id=%s, county_id = %s, state_id=%s, number_served=%s, url=%s'
                               'WHERE source_id=%s',
                               (utility_name, db_city, county, state_id, number_people_served, url, result[0]))
            self.connection.commit()
            cursor.close()
        except Exception as e:
            with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
                f.write("ERROR: {}; utilcode: {}; utilName: {}".format(e, response.meta["utility_code"], response.meta["utility_name"]))
            print("ERROR: {}; utilcode: {}; utilName: {}".format(e, response.meta["utility_code"], response.meta["utility_name"]))

    # this finds and writes all the info required for the sources table, and for the states table
    def scrape_source_info(self, response):
        try:
            util_code = response.url.split('=')[1]
            utility_name = response.xpath("//h1/text()").get()
            scraped_city = response.xpath("//ul[@class='served-ul']/li[1]/h2/text()").get().split(',')[0]
            url = response.url

            if len(scraped_city.split(' ')) <= 1 or scraped_city.split(' ')[len(scraped_city.split(' '))-1] != 'County':

                state_id = util_code[0:2]
                number_people_served = int(response.xpath(
                    "//ul[@class='served-ul']/li[2]/h2/text()").get().split(' ')[1].replace(',', ''))

                processed_utility_name = utility_name
                for i in range(len(utility_name)):
                    if utility_name[i] == '#':
                        processed_utility_name = utility_name[0:i]

                city_name_url = "https://www.ewg.org/tapwater/search-results.php?systemname={}&stab={}&" \
                                "searchtype=systemname".format(utility_name, state_id)
                yield scrapy.Request(url=city_name_url, callback=self.scrape_city_name, dont_filter=True, meta={
                    "utility_name": processed_utility_name, "state_id": state_id,
                    "number_people_served": number_people_served, "scraped_city": scraped_city, "util_code": util_code, "url": url})

        except Exception as e:
            with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
                f.write("\nERROR: {}. Source Code: {}".format(e, response.url.split('=')[1]))
            print("ERROR: {}. Source Code: {}".format(e, response.url.split('=')[1]))
