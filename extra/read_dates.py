from time import sleep
import csv

path = 'Belmont-Dates-2022.csv'

file = open(path, 'r')
reader = csv.reader(file)

for row in reader:
	sleep(1)
	print(row)


