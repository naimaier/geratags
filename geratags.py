import csv
from sys import argv, exit
from os import path


def input_file_is_valid(input_file_name):

    # Check if input file exists
    if not path.exists(input_file_name):
        print(f"O arquivo '{input_file_name}' nao existe")
        return False

    # Check if input file has csv extension
    if not input_file_name.endswith('.csv'):
        print(f"'{input_file_name}' nao e um arquivo csv valido!")
        return False

    return True


def template_file_is_valid(template_file_name):
    
    # Check if template file exists
    if not path.exists(template_file_name):
        print(f"O arquivo '{template_file_name}' nao existe")
        return False

    # Check if template file has txt extension
    if not template_file_name.endswith('.txt'):
        print(f"'{template_file_name}' nao e um arquivo txt valido!")
        return False

    return True


def read_csv_file(input_file_name):
    
    input_data = []

    # Read csv file (csv extension)
    with open(input_file_name, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            dictionary = {
                "name": row[0],
                "id": row[1]
            }
            input_data.append(dictionary)
            
    return input_data


def read_template_file(template_file_name):

    template_data = []

    # Read template file (txt extension)
    with open(template_file_name) as template_file:
        template_data = template_file.readlines()

    return template_data


def generate_output_data(input_data, template_data):

    # Create a variable stripping the hifens of the name attribute
    symbol = input_data["name"].replace("-", '')

    output_data = {
        "file_name": symbol.lower(),
        "data": []
    }

    # Include first two lines common to every model
    output_data["data"].append("#ID:" + input_data["id"] + "\n")
    output_data["data"].append('#Name:"' + input_data["name"] + '"\n')

    # Generate the output data by replacing the wildcard with the symbol
    for data in template_data:
        output_data["data"].append(data.replace("$", symbol))

    return output_data


def write_output_file(output_data):

    file_name = output_data["file_name"]

    # Write file
    with open(f"{file_name}.mne", "w") as output_file:
        output_file.writelines(output_data["data"])


# Check for correct usage
if len(argv) != 3:
    print("Uso: python geratags.py entrada.csv modelo.txt")
    exit(1)

input_file_name = argv[1]
template_file_name = argv[2]

# Validate input file
if not input_file_is_valid(input_file_name):
    exit(1)

# Validate template file
if not template_file_is_valid(template_file_name):
    exit(1)

# Read the input file
input_data = read_csv_file(input_file_name)

# Read the template file
template_data = read_template_file(template_file_name)

# Write output files
for data in input_data:
    output_data = generate_output_data(data, template_data)
    write_output_file(output_data)

exit(0)