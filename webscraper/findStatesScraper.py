#!/usr/bin/env python3

import scrapy


class FindStates(scrapy.Spider):
    name = "findStatesScraper"

    def start_requests(self):
        urls = {
             "https://www.ewg.org/tapwater/advanced-search.php"
         }
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        try:
            info = response.css("option::attr(value)").getall()
            filename = './resultFiles/EWGStates.txt'
            with open(filename, 'wb') as f:
                for item in info:
                    f.write('https://www.ewg.org/tapwater/state.php?stab={}&searchtype=largesys\n'.format(item).encode())
        except Exception as e:
            print(e)
