import scrapy
import psycopg2
import vodadata.constants as vodaconstants


class LeadInfoScraper(scrapy.Spider):
    name = "LeadInfoScraper"

    connection = psycopg2.connect(
      dbname=vodaconstants.DBNAME,
      user=vodaconstants.USER,
      password=vodaconstants.PASSWORD,
      host=vodaconstants.HOST,
      port=vodaconstants.PORT
    )
    connection.set_session(autocommit=True)

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
            cursor.execute("SELECT * FROM contaminants WHERE contaminants.name = 'lead'")
            result = cursor.fetchone()

            if not result:
                cursor.execute("INSERT INTO contaminants "
                               "(name, legal_limit, summary,"
                               " long_health_concerns, health_guideline)"
                               " VALUES ('lead', 15, %s, %s, .2)",
                               (summary, long_health_concerns))
            self.connection.commit()
            cursor.close()
        except Exception as e:
            with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
                f.write("Second level ERROR: {}".format(e))
            print(e)

    def scrape_source_lead_data(self):


    def write_source_lead_data(self):


    def start_requests(self):
        with open("./vodadata/datafiles/AllContaminants.txt") as f:
            urls = f.read().splitlines()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
