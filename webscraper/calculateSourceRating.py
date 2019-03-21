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
        # cursor.execute("SELECT * FROM states WHERE states.state_id = (%s)", (state_id, ))
        cursor.execute("SELECT * FROM contaminants")
        for contaminant in cursor:
            sub_cursor = self.connection.cursor()
            sub_cursor.execute(
                "SELECT STDDEV(source_level) FROM source_levels WHERE source_levels.contaminant_id=%s",
                (contaminant[0],))
            self.contaminant_stdev_dict[contaminant[0]] = sub_cursor.fetchone()
            sub_cursor.close()
        print(self.contaminant_stdev_dict)
        cursor.close()

    def collect_contaminant_nat_avgs(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM contaminants")

        for contaminant in cursor:
            self.contaminant_nat_avg_dict[contaminant[0]] = contaminant[3]
        print(self.contaminant_nat_avg_dict)
        cursor.close()

    def find_scores(self):
        source_cursor = self.connection.cursor()
        source_cursor.execute("SELECT * FROM sources")
        score = 0
        for source in source_cursor:
            score = 0
            cont_cursor = self.connection.cursor()
            cont_cursor.execute("SELECT * FROM source_levels WHERE "
                               "source_levels.source_id = %s", (source[0],))
            for cont in cont_cursor:
                print(cont[0])
                print(cont[1])
            # level print(result[2])


if __name__ == '__main__':
    calculateRating = CalculateSourceRating()
    calculateRating.collect_contaminants_stdev()
    calculateRating.collect_contaminant_nat_avgs()
#    find_scores()
