import csv
import psycopg2
import traceback
import vodadata.constants as consts


class GetLocaleData:

    connection = psycopg2.connect(
      dbname=consts.dbname,
      user=consts.user,
      password=consts.password,
      host=consts.host,
      port=consts.port
    )
    connection.set_session(autocommit=True)

    print("getLocaleData DB Connection status: " + str(connection.closed))  # should be zero if connection is open

    def get_locale_data(self):
        try:
            with open('./vodadata/localeData_1.txt', encoding='utf8') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter='\t')
                for row in csv_reader:
                    self.write_state_data(state_id=row[4])
                    self.write_county_data(county_name=row[5], state_id=row[4])
                    self.write_city_data(city_name=row[2], state_id=row[4], county_name=row[5])

            with open('./vodadata/localeData_2.csv', encoding='utf8') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')

                next(csv_reader)
                for row in csv_reader:
                    self.write_state_data(state_id=row[2])
                    self.write_county_data(county_name=row[5], state_id=row[2])
                    self.write_city_data(city_name=row[1], state_id=row[2], county_name=row[5])

            with open('./vodadata/localeData_3.csv', encoding='utf8') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter='|')

                next(csv_reader)
                for row in csv_reader:
                    self.write_state_data(state_id=row[1])
                    self.write_county_data(county_name=row[3], state_id=row[1])
                    self.write_city_data(city_name=row[0], state_id=row[1], county_name=row[3])
                    self.write_city_data(city_name=row[4], state_id=row[1], county_name=row[3])

        except Exception:
            print("ERROR\n{}".format(traceback.format_exc()))

    def write_state_data(self, state_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM states WHERE states.state_id = %s", (state_id,))
        result = cursor.fetchone()

        # if the state does not already exist, add it
        if not result and state_id != 'PR' and state_id != 'VI' and state_id != '':
            cursor.execute("INSERT INTO states (state_id) VALUES (%s)", (state_id,))

        self.connection.commit()
        cursor.close()

    def write_county_data(self, county_name, state_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM counties WHERE counties.name = %s AND counties.state = %s",
                       (county_name, state_id))
        result = cursor.fetchone()

        # if the county does not already exist, add it
        if not result and state_id != 'PR' and state_id != 'VI' and state_id != '':
            cursor.execute("INSERT INTO counties (name, state) VALUES (%s, %s)", (county_name, state_id))

        self.connection.commit()
        cursor.close()

    def write_city_data(self, city_name, state_id, county_name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM cities WHERE cities.name = %s AND cities.state_id = %s", (city_name, state_id))
        result = cursor.fetchone()

        cursor.execute("SELECT id FROM counties WHERE counties.name = %s AND counties.state = %s",
                       (county_name, state_id))
        county_id = cursor.fetchone()

        # if the city does not already exist, add it
        if not result and state_id != 'PR' and state_id != 'VI' and state_id != '':
            cursor.execute("INSERT INTO cities (name, state_id, county_id) "
                           "VALUES (%s, %s, %s)", (city_name, state_id, county_id))

        self.connection.commit()
        cursor.close()

    def main(self):
        self.get_locale_data()


if __name__ == '__main__':
    getLocaleData = GetLocaleData()
    getLocaleData.main()
