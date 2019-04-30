import scrapy


class FindContaminants(scrapy.Spider):
    name = "findContaminantsScraper"

    def start_requests(self):
        open('./vodadata/datafiles/AllContaminants.txt', "w+").close()
        url = "https://www.ewg.org/tapwater/chemical-contaminants.php"
        yield scrapy.Request(url=url, callback=self.parse)

    @staticmethod
    def parse(response):
        try:
            info = response.xpath("//tr[@class='clickable-row']/@data-href").getall()

            with open('./vodadata/datafiles/AllContaminants.txt', 'a') as f:
                for item in info:
                    f.write('https://www.ewg.org/tapwater/{}#\n'.format(item))
        except Exception as e:
            with open('./vodadata/datafiles/debugLog.txt', 'a') as f:
                f.write("ERROR: {}".format(e))
