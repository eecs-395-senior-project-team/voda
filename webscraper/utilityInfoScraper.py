#!/usr/bin/env python3

import scrapy
import psycopg2
from psycopg2 import sql


class FindInfo(scrapy.Spider):
  name = "utilityInfoScraper"

  connection = psycopg2.connect(
      dbname="postgres",
      user="postgres",
      password="pswd",
      host="127.0.0.1",
      port="5432"
  )
  print("Connection status: " + str(connection.closed)) #should be zero if connection is open
  def start_requests(self):
      with open("./resultFiles/AllEWGUtilities.txt") as f:
          urls = f.read().splitlines()
      for url in urls:
          yield scrapy.Request(url=url, callback=self.parse)
      # url = "https://www.ewg.org/tapwater/system.php?pws=OH1800403"
      # yield scrapy.Request(url=url, callback=self.parse)


  #this finds and writes all the info required for the sources table, and for the states table
  def scrape_source_info(self, response):
      try:
          utilCode = response.url.split('=')[1]
          utilityName = response.xpath("//h1/text()").get()
          city = response.xpath("//ul[@class='served-ul']/li[1]/h2/text()").get().split(',')[0]
          stateID = utilCode[0:2]
          numberPeopleServed = int(response.xpath("//ul[@class='served-ul']/li[2]/h2/text()").get().split(' ')[1]
                                   .replace(',', ''))


          cursor = self.connection.cursor()
          cursor.execute("SELECT * FROM states WHERE states.state_id = (%s)", (stateID, ))
          result =cursor.fetchone()
          if not result:
               cursor.execute("INSERT INTO states (state_id) VALUES (%s)", (stateID, ))

          cursor.execute("SELECT * FROM sources WHERE sources.utility_name = (%s)", (utilityName, ))
          result = cursor.fetchone()
          if not result:
              cursor.execute("INSERT INTO sources (utility_name, city, state, number_served)"
                         " VALUES (%s, %s, %s, %s)",
                             (utilityName, city, stateID, int(numberPeopleServed)))
          else:
              cursor.execute("UPDATE sources SET "
                             "utility_name=(%s), city=(%s), state=(%s), number_served=(%s)"
                             "WHERE source_id=(%s)",
                             (utilityName, city, stateID, numberPeopleServed, result[0]))

          self.connection.commit()
          cursor.close()
      except Exception as e:
          with open('./debugLog.txt', 'a') as f:
              f.write("ERROR: {}".format(e))
          print(e)

  def parse(self, response):
      try:
          self.scrape_source_info(response)
          # print(response.url)

          #  nameOfProvider = response.xpath("//h1/text()").get()
          # city = response.xpath("//ul[@class='served-ul']/li[1]/h2/text()").get()
          # numberPeopleServed = response.xpath("//ul[@class='served-ul']/li[2]/h2/text()").get().split(' ')[1]
          # state = utilCode[0:2]
          # write to the db
          # cursor.execute("SELECT * FROM sources WHERE sources.source_id = %s", [utilCode])
          # results = cursor.fetchall()
          # if not results:
          #     cursor.execute("INSERT INTO sources (city, source_id, name, state) VALUES (%s, %s, %s, %s)",
          #                (city, utilCode, nameOfProvider, state))
          # self.connection.commit()
          # cursor.close()



          # cursor = self.connection.cursor()
          # contAboveGLRaw = response.xpath("//ul[@id='contams_above_hbl']/li/section[@class='contaminant-data']")
          # contAboveGL = ""
          # for cont in contAboveGLRaw:
          #     if cont.xpath(".//div[@class='health-guideline-ppb']/text()").get() is not None:
          #         contAboveGL += "\n" + cont.xpath("./div[1]/h3/text()").get() + ",\n" +\
          #            "HEALTH_GL: " + cont.xpath(".//div[@class='health-guideline-ppb']/text()").extract()[1] + ",\n" +\
          #            "NATIONAL_AVG: " + cont.xpath(".//div[@class='national-ppb-popup']/text()").get() + ",\n" +\
          #            "STATE_AVG: " + cont.xpath(".//div[@class='state-ppb-popup']/text()").get() + ",\n" +\
          #            "THIS_UTIL: " + cont.xpath(".//div[@class='this-utility-ppb-popup']/text()").get() + ";"
          #         healthGL = cont.xpath(".//div[@class='health-guideline-ppb']/text()").extract()[1]
          #         natAvg = cont.xpath(".//div[@class='national-ppb-popup']/text()").get()
          #         thisUtil = cont.xpath(".//div[@class='this-utility-ppb-popup']/text()").get()
          #         contName = cont.xpath("./div[1]/h3/text()").get()
          #
          #         cursor.execute("SELECT contaminant_id FROM contaminants"
          #                                     " WHERE contaminants.name='{}'".format(contName))
          #         results = cursor.fetchall()
          #
          #         if not results:
          #             cursor.execute("INSERT INTO contaminants (name, health_guideline, national_average) VALUES"
          #                            " (%s, %s, %s)", (contName, healthGL, natAvg))
          #             self.connection.commit()
          #             cursor.close()
          #         cursor = self.connection.cursor()
          #         # cursor.execute("UPDATE source_levels SET contaminant_id=%s, source_id=%s, contaminant_level=%s"
          #         #                , [results[0], utilCode, thisUtil])
          #
          #     elif cont.xpath(".//div[@class = 'slide-toggle']/p[1]/a[1]/text()").get() is not None:
          #         contAboveGL += "\n" + cont.xpath("./div[1]/h3/text()").get() + ",\n"\
          #            "RADIATION_DETECTED: " + cont.xpath(".//div[@class = 'slide-toggle']/p[1]/a[1]/text()").get() + ";"
          #         thisUtil = cont.xpath(".//div[@class = 'slide-toggle']/p[1]/a[1]/text()").get()
          #         contName = cont.xpath("./div[1]/h3/text()").get()
          #
          # self.connection.commit()
          # cursor.close()
          #
          # otherContDetRaw = response.xpath("//ul[@id='contams_other']/li/section[@class='contaminant-data']")
          # otherContDet = ""
          # for cont in otherContDetRaw:
          #     if cont.xpath(".//div[@class='this-utility-ppb-popup']/text()").get() is not None:
          #         otherContDet += "\n" + cont.xpath("./div[1]/h3/text()").get() + ",\n"\
          #            "NATIONAL_AVG: " + cont.xpath(".//div[@class='national-ppb-popup']/text()").get() + ",\n" +\
          #            "STATE_AVG: " + cont.xpath(".//div[@class='state-ppb-popup']/text()").get() + ",\n" +\
          #            "THIS_UTIL: " + cont.xpath(".//div[@class='this-utility-ppb-popup']/text()").get() + ";"
          #
          # otherContNotDet=""
          # otherContNotDetRaw = response.xpath("//section[@class='contams-not-detected']/div[2]/p[2]/a/text()").getall()
          # for cont in otherContNotDetRaw:
          #     otherContNotDet += "\n" + cont + ";"
          #
          # info = "{{{};{};{};{}\n\n" \
          #        "CONT_ABOVE_GL:({})\n\n" \
          #        "OTHER_CONT_DETECTED:({})\n\n" \
          #        "OTHER_NOT_DETECTED:({})}}\n\n".format\
          #     (utilCode, nameOfProvider, city, numberPeopleServed, contAboveGL, otherContDet, otherContNotDet)
          #
          #
          #
          # self.connection.close()
          # with open('./resultFiles/FinalInfoTest.txt', 'a') as f:
          #     f.write(info)

      except Exception as e:
          # with open('./resultFiles/FinalInfoTest.txt', 'a') as f:
          #     f.write("ERROR: {}".format(e))
          print(e)

