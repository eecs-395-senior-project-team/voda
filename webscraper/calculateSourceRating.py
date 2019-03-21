import psycopg2


name = "utilityInfoScraper"

connection = psycopg2.connect(
  dbname="postgres",
  user="postgres",
  password="pswd",
  host="127.0.0.1",
  port="5432"
)
connection.set_session(autocommit=True)

contaminant_stdev_dict = {}
contaminant_nat_avg_dict = {}


def collect_contaminants_stdev():
    cursor = connection.cursor()
    # cursor.execute("SELECT * FROM states WHERE states.state_id = (%s)", (state_id, ))
    cursor.execute("SELECT * FROM contaminants")

    for contaminant in cursor:
        sub_cursor = connection.cursor()
        print(contaminant[0])
        contaminant_stdev_dict[contaminant[0]] = sub_cursor.execute(
            "SELECT STDDEV(source_level) FROM source_levels WHERE source_levels.contaminant_id=%s", (contaminant[0],))
        results = sub_cursor.execute("SELECT * FROM source_levels WHERE source_levels.contaminant_id=%s", (contaminant[0],))
        print(results)
        sub_cursor.close()
    print(len(contaminant_stdev_dict))
    print(contaminant_stdev_dict.values())
    cursor.close()

def collect_contaminant_nat_avgs():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM contaminants")

    for contaminant in cursor:
        contaminant_nat_avg_dict[contaminant[0]] = contaminant[3]
    cursor.close()

def find_scores():
    source_cursor = connection.cursor()
    source_cursor.execute("SELECT * FROM sources")
    score = 0
    for source in source_cursor:
        score = 0
        cont_cursor = connection.cursor()
        cont_cursor.execute("SELECT * FROM source_levels WHERE "
                           "source_levels.source_id = %s", (source[0],))
        for cont in cont_cursor:
            print(cont[0])
            print(cont[1])
        # level print(result[2])

if __name__ == '__main__':
    collect_contaminants_stdev()
    collect_contaminant_nat_avgs()
#    find_scores()
