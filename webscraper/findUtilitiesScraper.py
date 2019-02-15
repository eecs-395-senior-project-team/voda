#!/usr/bin/env python3

import scrapy


class FindUtilities(scrapy.Spider):
    name = "findUtilitiesScraper"
    open('./resultFiles/AllEWGUtilities.txt', "w").close()

    def start_requests(self):
        with open("./resultFiles/EWGStates.txt") as f:
            urls = f.read().splitlines()
        urld = {
            "https://www.ewg.org/tapwater/state.php?stab=AL&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=US&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=AL&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=AK&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=AZ&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=AR&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=CA&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=CO&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=CT&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=DE&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=DC&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=FL&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=GA&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=HI&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=ID&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=IL&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=IN&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=IA&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=KS&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=KY&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=LA&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=ME&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=MD&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=MA&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=MI&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=MN&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=MS&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=MO&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=MT&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=NE&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=NV&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=NH&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=NJ&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=NM&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=NY&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=NC&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=ND&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=OH&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=OK&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=OR&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=PA&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=RI&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=SC&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=SD&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=TN&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=TX&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=UT&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=VT&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=VA&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=WA&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=WV&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=WI&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=WY&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=US&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=AL&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=AK&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=AZ&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=AR&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=CA&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=CO&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=CT&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=DE&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=DC&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=FL&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=GA&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=HI&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=ID&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=IL&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=IN&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=IA&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=KS&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=KY&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=LA&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=ME&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=MD&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=MA&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=MI&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=MN&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=MS&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=MO&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=MT&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=NE&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=NV&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=NH&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=NJ&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=NM&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=NY&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=NC&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=ND&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=OH&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=OK&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=OR&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=PA&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=RI&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=SC&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=SD&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=TN&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=TX&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=UT&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=VT&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=VA&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=WA&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=WV&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=WI&searchtype=largesys",
            "https://www.ewg.org/tapwater/state.php?stab=WY&searchtype=largesys",

        }

        for url in urls:
            print(url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        try:
            info = response.xpath("//table/tbody/tr/td/a[contains(@href,'system')]/@href").getall()
            print(info)

            with open('./resultFiles/AllEWGUtilities.txt', 'a') as f:
                for item in info:
                    f.write('https://www.ewg.org/tapwater/{}\n'.format(item))
        except Exception as e:
            print(e)
