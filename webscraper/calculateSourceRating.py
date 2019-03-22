import psycopg2


class CalculateSourceRating(object):
    connection = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="pswd",
        host="127.0.0.1",
        port="5432"
    )
    connection.set_session(autocommit=True)

    print("Connection status: " + str(connection.closed))  # should be zero if connection is open
    contaminant_stdev_dict = {}
    contaminant_nat_avg_dict = {}

    def collect_contaminants_stdev(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM contaminants")
        for contaminant in cursor:
            sub_cursor = self.connection.cursor()
            sub_cursor.execute(
                "SELECT source_level FROM source_levels WHERE source_levels.contaminant_id=%s",
                (contaminant[0],))
            # STDDEV(source_level)
            self.contaminant_stdev_dict[contaminant[0]] = sub_cursor.fetchone()
            sub_cursor.close()
        cursor.close()

    def collect_contaminant_nat_avgs(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM contaminants")

        for contaminant in cursor:
            self.contaminant_nat_avg_dict[contaminant[0]] = contaminant[3]
        cursor.close()

    def find_scores(self):
        source_cursor = self.connection.cursor()
        source_cursor.execute("SELECT * FROM sources")
        for source in source_cursor:
            rating = 0
            cont_cursor = self.connection.cursor()
            cont_cursor.execute("SELECT * FROM source_levels WHERE "
                               "source_levels.source_id = %s", (source[0],))
            for cont in cont_cursor:
                # amount above the national average
                if cont[2] is not None:
                    amount_above_average = cont[2] - self.contaminant_nat_avg_dict[cont[0]]
                    if self.contaminant_stdev_dict[cont[0]] is not None:
                        amount_to_add = amount_above_average / self.contaminant_stdev_dict.get(cont[0])[0]
                        if amount_to_add > 0:
                            rating = rating + amount_to_add

            cont_cursor = self.connection.cursor()
            cont_cursor.execute("UPDATE sources SET rating = %s WHERE source_id = %s", (rating, source[0]))
            cont_cursor.close()
        source_cursor.close()


if __name__ == '__main__':
    calculateRating = CalculateSourceRating()
    calculateRating.collect_contaminants_stdev()
    calculateRating.collect_contaminant_nat_avgs()
    calculateRating.find_scores()
