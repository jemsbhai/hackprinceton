import csv

path = "40PlusDevs.tsv.txt"

with open(path, encoding='utf-8') as f:
    reader = csv.reader(f, delimiter="\t")
    for row in reader:
        print (row[6])



