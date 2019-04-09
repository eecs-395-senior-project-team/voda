import scrapy
import csv


class FindUtilities(scrapy.Spider):
    name = "findUtilitiesScraper"
    open('./vodadata/AllEWGUtilities.txt', "w").close()

    def start_requests(self):
        with open("./vodadata/zipCodes.txt", encoding='utf8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')

            for row in csv_reader:
                url = "https://www.ewg.org/tapwater/search-results.php?zip5={}&searchtype=zip".format(row[0])
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        try:
            info = response.xpath("//figure[@class='search-results-figure'][2]/table/tbody/tr/td/a[contains"
                                  "(@href,'system')]/@href").getall()

            with open('./vodadata/AllEWGUtilities.txt', 'a') as f:
                for item in info:
                    f.write('https://www.ewg.org/tapwater/{}\n'.format(item))
        except Exception as e:
            print(e)
