import csv
from sys import argv, exit
from os import path

def input_file_is_valid(filename):

    # Check if input file exists
    if not path.exists(input_file_name):
        print(f"O arquivo '{input_file_name}' nao existe")
        return False

    # Check if input file is of csv extension
    if not input_file_name.endswith('.csv'):
        print(f"'{input_file_name}' nao e um arquivo csv valido!")
        return False

    return True


def read_csv_file(filename):
    
    input_data = []

    # Read csv file
    with open(input_file_name, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            dictionary = {
                "name": row[0],
                "id": row[1]
            }
            input_data.append(dictionary)
            
    return input_data


# Check for correct usage
if len(argv) != 2:
    print("Uso: python geratags.py entrada.csv")
    exit(1)

input_file_name = argv[1]

# Validate input file
if not input_file_is_valid(input_file_name):
    exit(1)

# Read the input file
input_data = read_csv_file(input_file_name)

exit(0)