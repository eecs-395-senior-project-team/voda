import psycopg2
import signal
import sys


class CalculateSourceRating:
    contaminant_std_dev_dict = {}
    contaminant_nat_avg_dict = {}

    def __init__(self, connection):
        self.connection = connection

    def collect_contaminants_stdev(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM "vodaMainApp_contaminants"')
        for contaminant in cursor:
            sub_cursor = self.connection.cursor()
            sub_cursor.execute(
                'SELECT STDDEV(source_level) FROM "vodaMainApp_source_levels" WHERE contaminant_id=%s',
                (contaminant[0],))
            self.contaminant_std_dev_dict[contaminant[0]] = sub_cursor.fetchone()
            sub_cursor.close()
        cursor.close()

    def collect_contaminant_nat_avgs(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM "vodaMainApp_contaminants"')

        for contaminant in cursor:
            self.contaminant_nat_avg_dict[contaminant[0]] = contaminant[3]
        cursor.close()

    def amount_above_avg(self, cont):
        return cont[2] - self.contaminant_nat_avg_dict[cont[0]]

    def amount_to_add(self, cont, amt_above_average):
        if self.contaminant_std_dev_dict[cont[0]][0] is not None:
            if self.contaminant_std_dev_dict.get(cont[0])[0] != 0:
                amount_to_add = amt_above_average / self.contaminant_std_dev_dict.get(cont[0])[0]
            else:
                amount_to_add = amt_above_average
            return amount_to_add

    def find_scores(self):
        source_cursor = self.connection.cursor()
        source_cursor.execute('SELECT * FROM "vodaMainApp_sources"')
        for source in source_cursor:
            rating = 0
            cont_cursor = self.connection.cursor()
            cont_cursor.execute('SELECT * FROM "vodaMainApp_source_levels" WHERE '
                                'source_id = %s', (source[0],))
            for cont in cont_cursor:
                # amount above the national average
                if cont[2] is not None:
                    # amount_above_average = cont[2] - self.contaminant_nat_avg_dict[cont[0]]
                    amount_above_average = self.amount_above_avg(cont)
                    amt_to_add = self.amount_to_add(rating, cont, amount_above_average)

                    if amt_to_add > 0:
                        rating + amt_to_add

            cont_cursor = self.connection.cursor()
            cont_cursor.execute('UPDATE "vodaMainApp_sources" SET rating = %s WHERE source_id = %s', (rating, source[0]))
            cont_cursor.close()
        source_cursor.close()

    @staticmethod
    def signal_handler(sig, frame):
        sys.exit(0)

    def main(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        self.collect_contaminants_stdev()
        self.collect_contaminant_nat_avgs()
        self.find_scores()
