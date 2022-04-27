import csv
lines = list()
with open(r"scrapped/Scrapped.csv", encoding='UTF-8') as f:  #Enter your file name
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    output = open('scrapped/Scrapped_edit.csv', 'wb')
    writer = csv.writer(output)
    next(rows, None)
    for row in rows:
        if row[0] is not None and len(row[0]) > 0:
            lines.append(row)

with open(r'scrapped/Scrapped.csv', 'w') as write_file:
    writer = csv.writer(write_file)
    writer.writerows(lines)