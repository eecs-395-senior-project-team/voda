#!/usr/bin/env python3

import scrapy


class FindInfo(scrapy.Spider):
    name = "utilityInfoScraper"
    open('./resultFiles/FinalInfo.txt', "w").close()

    def start_requests(self):
        with open("./resultFiles/AllEWGUtilities.txt") as f:
            urls = f.read().splitlines()

        # yield scrapy.Request(url=urls[0], callback=self.parse)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        try:
            print(response.url)
            utilCode = response.url.split('=')[1]
            nameOfProvider = response.xpath("//h1/text()").get()
            city = response.xpath("//ul[@class='served-ul']/li[1]/h2/text()").get()
            numberPeopleServed = response.xpath("//ul[@class='served-ul']/li[2]/h2/text()").get().split(' ')[1]

            contAboveGLRaw = response.xpath("//ul[@id='contams_above_hbl']/li/section[@class='contaminant-data']")
            contAboveGL = ""
            for cont in contAboveGLRaw:
                contAboveGL += "\n" + cont.xpath("./div[1]/h3/text()").get() + ",\n"\
                   "HEALTH_GL: " + cont.xpath(".//div[@class='health-guideline-ppb']/text()").extract()[1] + ",\n" +\
                   "NATIONAL_AVG: " + cont.xpath(".//div[@class='national-ppb-popup']/text()").get() + ",\n" +\
                   "STATE_AVG: " + cont.xpath(".//div[@class='state-ppb-popup']/text()").get() + ",\n" +\
                   "THIS_UTIL: " + cont.xpath(".//div[@class='this-utility-ppb-popup']/text()").get() + ";"

            otherContDetRaw = response.xpath("//ul[@id='contams_other']/li/section[@class='contaminant-data']")
            otherContDet = ""
            # for cont in otherContDetRaw:
            #     otherContDet += "\n" + cont.xpath("./div[1]/h3/text()").get() + ",\n"\
            #        "NATIONAL_AVG: " + cont.xpath(".//div[@class='national-ppb-popup']/text()").get() + ",\n" +\
            #        "STATE_AVG: " + cont.xpath(".//div[@class='state-ppb-popup']/text()").get() + ",\n" +\
            #        "THIS_UTIL: " + cont.xpath(".//div[@class='this-utility-ppb-popup']/text()").get() + ";"

            otherContNotDet=""
            otherContNotDetRaw = response.xpath("//section[@class='contams-not-detected']/div[2]/p[2]/a/text()").getall()
            for cont in otherContNotDetRaw:
                otherContNotDet += "\n" + cont + ";"
            info = "{{{};{};{};{}\n\n" \
                   "CONT_ABOVE_GL:({})\n\n" \
                   "OTHER_CONT_DETECTED:({})\n\n" \
                   "OTHER_NOT_DETECTED:({})}}\n\n".format\
                (utilCode, nameOfProvider, city, numberPeopleServed, contAboveGL, otherContDet, otherContNotDet)
            # print(utilCode)
            # print(nameOfProvider)
            # print(city)
            # print(numberPeopleServed)

            with open('./resultFiles/FinalInfo.txt', 'a') as f:
                f.write(info)

        except Exception as e:
            print(e)
