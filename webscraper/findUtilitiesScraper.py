#!/usr/bin/env python3

import scrapy


class FindUtilities(scrapy.Spider):
    name = "findUtilitiesScraper"
    open('./resultFiles/AllEWGUtilities.txt', "w").close()

    def start_requests(self):
        with open("./resultFiles/EWGStates.txt") as f:
            urls = f.read().splitlines()

        for url in urls:
            print(url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        try:
            info = response.xpath("//table/tbody/tr/td/a[contains(@href,'system')]/@href").getall()

            with open('./resultFiles/AllEWGUtilities.txt', 'a') as f:
                for item in info:
                    f.write('https://www.ewg.org/tapwater/{}\n'.format(item))
        except Exception as e:
            print(e)
