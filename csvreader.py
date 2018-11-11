import csv

f = open('harassment_data_train.csv')
csv_f = csv.reader(f)

for row in csv_f:
  ##print (row)
  if row[1] == "harassment":
      print (row[0])
