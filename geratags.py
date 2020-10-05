# coding: utf-8
import csv
from os import path
from tkinter import Tk, Label, Button, messagebox
from tkinter.filedialog import askopenfilename, askdirectory
from functools import partial
import json


def load_settings():
    settings = {}
    with open("settings.json", "r") as settings_file:
        settings = json.load(settings_file)

    return settings


def write_settings(settings):
    with open("settings.json", "w") as settings_file:
        json.dump(settings, settings_file)


def input_file_is_valid(input_file_name):
    # Check if input file exists
    if not path.exists(input_file_name):
        print("O arquivo '" + input_file_name + "' não existe")
        return False

    return True


def template_file_is_valid(template_file_name):
    # Check if template file exists
    if not path.exists(template_file_name):
        print("O arquivo '" + template_file_name + "' não existe")
        return False

    return True


def export_path_is_valid(export_path):
    # Check if template file exists
    if not path.exists(export_path):
        print("O arquivo '" + export_path + "' não existe")
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
    # Write file
    with open(output_data["file_name"] + ".mne", "w") as output_file:
        output_file.writelines(output_data["data"])


def bt_input_click(settings, lb):
    # TODO change initial dir to 'C:\'
    settings["input_file"] = askopenfilename(initialdir='/', 
                                             title='Selecione o Arquivo de Entrada', 
                                             filetypes=[('Arquivos CSV', '*.csv')])
    lb["text"] = settings["input_file"]
    write_settings(settings)


def bt_template_click(settings, lb):
    # TODO change initial dir to 'C:\'
    settings["template_file"] = askopenfilename(initialdir='/', 
                                             title='Selecione o Arquivo de Modelo', 
                                             filetypes=[('Arquivos TXT', '*.txt')])
    lb["text"] = settings["template_file"]
    write_settings(settings)


def bt_export_path_click(settings, lb):
    # TODO change initial dir to 'C:\'
    settings["export_path"] = askdirectory(initialdir='/', 
                                           title='Selecione o Diretório de Destino')
    lb["text"] = settings["export_path"]
    write_settings(settings)


def bt_run_click(settings):
    # Validate input file
    if not input_file_is_valid(settings["input_file"]):
        return

    # Validate template file
    if not template_file_is_valid(settings["template_file"]):
        return
    
    # Validate export path
    if not export_path_is_valid(settings["export_path"]):
        return
    
    # Read the input file
    input_data = read_csv_file(settings["input_file"])

    # Read the template file
    template_data = read_template_file(settings["template_file"])

    # Write output files
    for data in input_data:
        output_data = generate_output_data(data, template_data)
        write_output_file(output_data)
    
    messagebox.showinfo("Arquivos gerados", "Arquivos gerados")


if path.exists("settings.json"):
    settings = load_settings()
else:
    settings = {
        'input_file': 'Escolher',
        'template_file': 'Escolher',
        'export_path': 'Escolher'
    }

# Generate main window
root = Tk()

root.title("Gerador de Tags")

lb_input = Label(root, text=settings["input_file"])
lb_input.grid(row=0, column=1)

bt_input = Button(root, text="Arquivo de Entrada")
bt_input["command"] = partial(bt_input_click, settings, lb_input)
bt_input.grid(row=0, column=0)

lb_template = Label(root, text=settings["template_file"])
lb_template.grid(row=1, column=1)

bt_template = Button(root, text="Arquivo de Modelo")
bt_template["command"] = partial(bt_template_click, settings, lb_template)
bt_template.grid(row=1, column=0)

lb_export_path = Label(root, text=settings["export_path"])
lb_export_path.grid(row=2, column=1)

bt_export_path = Button(root, text="Caminho de Destino")
bt_export_path["command"] = partial(bt_export_path_click, settings, lb_export_path)
bt_export_path.grid(row=2, column=0)

bt_run = Button(root, text="Gerar Arquivos")
bt_run["command"] = partial(bt_run_click, settings)
bt_run.grid(row=3, column=0, columnspan=2)

root.mainloop()