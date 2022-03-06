import csv

with open(r"question.csv", encoding='UTF-8') as f:
    rows = csv.reader(f, delimiter=",", lineterminator="\n")
    for row in rows:
        print(row[0])
        break
    # rows = list(rows)
    # message = rows[3][0]
    # print(len(rows))