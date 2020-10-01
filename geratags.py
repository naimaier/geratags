import csv
from sys import argv, exit
from os import path
from helpers import *


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


def write_output_file(output_data):
    # TODO change file name
    file_name = output_data["#Name"].replace('"', "").replace("-", "").lower()

    with open(f"{file_name}.mne", "w") as output_file:
        for key, value in output_data.items():
            output_file.write(str(key) + ':'+ str(value) + '\n') 
    

# Check for correct usage
if len(argv) != 3:
    print("Uso: python geratags.py entrada.csv #format")
    exit(1)

input_file_name = argv[1]
model_numer = int(argv[2])

# Validate input file
if not input_file_is_valid(input_file_name):
    exit(1)

# Read the input file
input_data = read_csv_file(input_file_name)

# Write output files
for data in input_data:
    output_data = generate(data, model_numer)
    write_output_file(output_data)

exit(0)