import scrapy


class FindContaminants(scrapy.Spider):
    name = "findContaminantsScraper"
    open('./vodaData/AllContaminants.txt', "w").close()
    with open('./vodaData/debugLog.txt', 'a') as f:
        f.write("test")

    def start_requests(self):
        url = "https://www.ewg.org/tapwater/chemical-contaminants.php"
        yield scrapy.Request(url=url, callback=self.parse)

    @staticmethod
    def parse(response):
        with open('./vodaData/debugLog.txt', 'a') as f:
            f.write("test1")
        try:
            info = response.xpath("//tr[@class='clickable-row']/@data-href").getall()

            with open('./vodaData/AllContaminants.txt', 'a') as f:
                for item in info:
                    f.write('https://www.ewg.org/tapwater/{}#\n'.format(item))
        except Exception as e:
            with open('./vodaData/debugLog.txt', 'a') as f:
                f.write("ERROR: {}".format(e))
