import csv
import psycopg2
import traceback


class GetLocaleData:

    def __init__(self, connection):
        self.connection = connection

    def get_locale_data(self):
        try:
            with open('./vodadata/datafiles/localeData_2.csv', encoding='utf8') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')

                next(csv_reader)
                for row in csv_reader:
                    self.write_state_data(state_id=row[2])
                    self.write_county_data(county_id=row[4], county_name=row[5].title(), state_id=row[2])
                    self.write_city_data(city_name=row[1].title(), state_id=row[2], county_name=row[5].title())

            with open('./vodadata/datafiles/localeData_1.txt', encoding='utf8') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter='\t')
                for row in csv_reader:
                    self.write_state_data(state_id=row[4])
                    self.write_city_data(city_name=row[2].title(), state_id=row[4], county_name=row[5].title())

            with open('./vodadata/datafiles/localeData_3.csv', encoding='utf8') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter='|')

                next(csv_reader)
                for row in csv_reader:
                    self.write_state_data(state_id=row[1])
                    self.write_city_data(city_name=row[0].title(), state_id=row[1], county_name=row[3].title())
                    self.write_city_data(city_name=row[4].title(), state_id=row[1], county_name=row[3].title())

        except Exception:
            print('ERROR\n{}'.format(traceback.format_exc()))

    def write_state_data(self, state_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM "vodaMainApp_states" WHERE state_id = %s', (state_id,))
            result = cursor.fetchone()

            # if the state does not already exist, add it
            if not result and state_id != 'PR' and state_id != 'VI' and state_id != '':
                cursor.execute('INSERT INTO "vodaMainApp_states" (state_id) VALUES (%s)', (state_id,))

            self.connection.commit()
            cursor.close()
        except Exception:
            print('ERROR\n{}'.format(traceback.format_exc()))

    def write_county_data(self, county_id, county_name, state_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM "vodaMainApp_counties" WHERE id=%s',
                           (county_id,))
            result = cursor.fetchone()

            # if the county does not already exist, add it
            if not result and state_id != 'PR' and state_id != 'VI' and state_id != '':
                cursor.execute('INSERT INTO "vodaMainApp_counties" (id, name, state_id) VALUES (%s, %s, %s)', (county_id, county_name, state_id))

            self.connection.commit()
            cursor.close()
        except Exception:
            print('ERROR\n{}'.format(traceback.format_exc()))

    def write_city_data(self, city_name, state_id, county_name):
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM "vodaMainApp_cities" WHERE name = %s AND state_id = %s', (city_name, state_id))
            result = cursor.fetchone()

            cursor.execute('SELECT id FROM "vodaMainApp_counties" WHERE name = %s AND state_id = %s',
                           (county_name, state_id))
            county_id = cursor.fetchone()

            if county_id is None and state_id != 'PR' and state_id != 'VI' and state_id != '':
                pass

            # if the city does not already exist, add it
            elif not result and state_id != 'PR' and state_id != 'VI' and state_id != '':
                cursor.execute('INSERT INTO "vodaMainApp_cities" (name, state_id, county_id) '
                               'VALUES (%s, %s, %s)', (city_name, state_id, county_id))

            self.connection.commit()
            cursor.close()

        except Exception:
            print('ERROR\n{}'.format(traceback.format_exc()))

    def main(self):
        self.get_locale_data()


if __name__ == '__main__':
    getLocaleData = GetLocaleData()
    getLocaleData.main()
