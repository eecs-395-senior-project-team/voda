import psycopg2


def collect_contaminants_stdev(connection, stdev_dict):
    cursor = connection.cursor()
    # cursor.execute("SELECT * FROM states WHERE states.state_id = (%s)", (state_id, ))
    # cursor.execute("SELECT * FROM contaminants")
    print(cursor.execute("SELECT * FROM source_levels"))
    print(cursor.execute("SELECT * FROM contaminants"))
    # for contaminant in cursor:
    #     sub_cursor = connection.cursor()
    #     print(contaminant[0])
    #     contaminant_stdev_dict[contaminant[0]] = sub_cursor.execute(
    #         "SELECT STDDEV(source_level) FROM source_levels WHERE source_levels.contaminant_id=(%s)", (contaminant[0],))
    #     results = sub_cursor.execute("SELECT * FROM source_levels WHERE source_levels.contaminant_id=(%s)", (110,))
    #     print(results)
    #     sub_cursor.close()
    # print(contaminant_stdev_dict.values())
    cursor.close()

def collect_contaminant_nat_avgs(connection, nat_avg_dict):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM contaminants")

    for contaminant in cursor:
        contaminant_nat_avg_dict[contaminant[0]] = contaminant[3]
    cursor.close()

def find_scores(connection):
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

    collect_contaminants_stdev(connection, contaminant_stdev_dict)
    collect_contaminant_nat_avgs(connection, contaminant_nat_avg_dict)
#    find_scores()
