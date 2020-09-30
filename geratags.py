import csv
from sys import argv, exit
from os import path

# Check for correct usage
if len(argv) != 2:
    print("Uso: python geratags.py entrada.csv")
    exit(1)

input_file_name = argv[1]

# Check if input file exists
if not path.exists(input_file_name):
    print(f"O arquivo '{input_file_name}' nao existe")
    exit(1)

# Check if input file is of csv extension
if not input_file_name.endswith('.csv'):
    print(f"'{input_file_name}' nao e um arquivo csv valido!")
    exit(1)

# Read csv file
with open(input_file_name, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        print(row)

exit(0)