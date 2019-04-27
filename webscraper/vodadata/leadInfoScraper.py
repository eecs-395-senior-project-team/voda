import scrapy
import psycopg2


class LeadInfoScraper(scrapy.Spider):
    name = "LeadInfoScraper"

    def __init__(self, connection):
        self.connection = connection

    def write_lead_to_contaminants(self):
        long_health_concerns = "Complying with the EPA's lead rules doesn't mean that the water is safe for " \
                               "children to drink. " \
                  "The EPA’s recent modeling suggests that lead concentrations in the 3.8 to 15 ppb range can put a " \
                  "formula-fed baby at risk of elevated blood lead levels. In 2009, the California Office of " \
                  "Environmental Health Hazard Assessment set a public health goal level of 0.2 ppb for lead in " \
                  "drinking water to protect against even subtle IQ loss in children."

        summary = "Since 2014, and the crisis that rocked the community of Flint, Mich., lead in" \
                               " drinking water has been a topic thrust into the headlines and the minds of " \
                               "millions of Americans." \
                               "On Aug. 14, 2014 a water boil advisory was declared for certain parts of the city. " \
                               "In response to coliform contamination, the city of Flint decided to switch " \
                               "the source " \
                               "of its drinking water. What occurred over the next three years amounted to one of " \
                               "the " \
                               "largest infrastructure and government failures regarding public health in modern " \
                               "American history. Due to the introduction of highly acidic water from the Flint River" \
                               " and insufficient water treatment techniques, children who consumed this " \
                               "lead-tainted " \
                               "water had 46 percent higher blood lead levels than children in nearby Detroit. It" \
                               " has " \
                               "been estimated roughly 12,000 Flint children were exposed to water with high levels" \
                               " of " \
                               "lead. Since Flint, many other areas of the country have demanded better testing for " \
                               "lead in their homes and communities. Lead contamination has been found to be a " \
                               "nationwide issue – whether in a small community like St. Josephs, La., an affluent " \
                               "suburb such as San Marino, Calif., or major metropolitan locations like New York " \
                               "City and Chicago."
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM "vodaMainApp_contaminants" WHERE name = "lead"')
            result = cursor.fetchone()

            if not result:
                cursor.execute('INSERT INTO "vodaMainApp_contaminants" '
                               '(name, legal_limit, summary,'
                               ' long_health_concerns, health_guideline)'
                               ' VALUES ('lead', 15, %s, %s, .2)',
                               (summary, long_health_concerns))
            self.connection.commit()
            cursor.close()
        except Exception as e:
            with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
                f.write("Second level ERROR: {}".format(e))
            print(e)

    def scrape_source_lead_data(self, response):
        source_name = response.xpath("//h2[@class='systemname-h2']/text()").get().split('-')[0]
        source_state = response.url.split('=')[1][0:2]
        cursor = self.connection.cursor()
        cursor.execute('SELECT source_id FROM "vodaMainApp_sources" WHERE utility_name = %s AND state = %s',
                       (source_name, source_state))
        src_id = cursor.fetchone()
        cursor.close()
        this_utility_value = 0.0
        if response.xpath("//p/b[contains(text(), '90 percent of lead samples collected')]") is not None:
            this_utility_value = response.xpath("//p/b[contains(text(),'90 percent of lead samples collected')]").get(
            ).split("parts")[0].split("below")[1]

        elif response.xpath("//table[@class = 'system-contaminant-table']") is not None:
            counter = 0
            total = 0
            set = response.xpath("//table[@class = 'system-contaminant-table']/tbody/tr/td[@data-label='Result']")
            for result in set:
                counter = counter + 1
                if result.xpath("//b/text()") is not None:
                    result_num = result.xpath("//b/text()").get().split(" ")[0]
                else:
                    result_num = result.xpath("//text()").get().split(" ")[0]
                if result_num != 'ND':
                    total = total + result_num
            this_utility_value = total/counter
        self.write_source_lead_data('lead', src_id, this_utility_value)

    def write_source_lead_data(self, cont_name, src_id, this_utility_value):
        cursor = self.connection.cursor()

        # get the id of this contaminant based on its name
        cursor.execute('SELECT contaminant_id FROM "vodaMainApp_contaminants" WHERE name = %s',
                       (cont_name,))
        cont_id = cursor.fetchone()

        # check if this source-contaminant relationship exists
        cursor.execute('SELECT * FROM "vodaMainApp_source_levels" WHERE source_id = %s '
                       'AND contaminant_id = %s", (src_id, cont_id))
        results = cursor.fetchall()

        # if there is not already a row for this contaminant-utility pair, add one,
        if not results:
            cursor.execute('INSERT INTO "vodaMainApp_source_levels" (source_id, contaminant_id, source_level)'
                           ' VALUES (%s, %s, %s)', (src_id, cont_id, this_utility_value))
        # otherwise update the values
        else:
            cursor.execute('UPDATE "vodaMainApp_source_levels" SET source_level=%s WHERE source_id=%s AND contaminant_id=%s',
                           (this_utility_value, src_id, cont_id))
        cursor.close()

    def start_requests(self):
        self.write_lead_to_contaminants()

        with open("./vodadata/datafiles/AllEWGUtilities.txt") as f:
            urls = f.read().splitlines()
        for url in urls:
            url = 'https://www.ewg.org/tapwater/what-about-lead.php?pws={}'.format(url.split('=')[1])
            yield scrapy.Request(url=url, callback=self.scrape_source_lead_data)
