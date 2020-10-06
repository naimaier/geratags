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


def export_path_is_valid(export_path):
    # Check if template file exists
    if not path.exists(export_path):
        messagebox.showwarning("O caminho '" + export_path + "' não existe")
        return False

    return True


def read_csv_file(input_file_name):
    input_data = []

    # Read csv file (csv extension)
    try:
        with open(input_file_name, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                dictionary = {
                    "name": row[0],
                    "id": row[1]
                }
                input_data.append(dictionary)

    except FileNotFoundError:
        messagebox.showerror('Erro', 'O arquivo ' + input_file_name + ' não existe')
        return None

    except:
        messagebox.showerror('Erro', 'Não foi possível abrir o arquivo de entrada: ' + input_file_name)
        return None

    return input_data


def read_template_file(template_file_name):
    template_data = []

    # Read template file (txt extension)
    try:
        with open(template_file_name) as template_file:
            template_data = template_file.readlines()

    except FileNotFoundError:
        messagebox.showerror('Erro', 'O arquivo ' + template_file_name + ' não existe')
        return None

    except:
        messagebox.showerror('Erro', 'Não foi possível abrir o arquivo de modelo: ' + template_file_name)
        return None

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


def write_output_file(settings, output_data):
    # Join the output file path and file name
    output_data['file_name'] = path.join(settings['export_path'], output_data['file_name'])

    # Write file
    with open(output_data["file_name"] + ".mne", "w") as output_file:
        output_file.writelines(output_data["data"])


def ask_for_input_file(settings, lb):
    settings["input_file"] = askopenfilename(initialdir=settings['input_file'], 
                                             title='Selecione o Arquivo de Entrada', 
                                             filetypes=[('Arquivos CSV', '*.csv')])
    if settings['input_file']:
        lb["text"] = settings["input_file"]
        write_settings(settings)


def ask_for_template_file(settings, lb):
    settings["template_file"] = askopenfilename(initialdir=settings['template_file'], 
                                             title='Selecione o Arquivo de Modelo', 
                                             filetypes=[('Arquivos TXT', '*.txt')])
    if settings['template_file']:
        lb["text"] = settings["template_file"]
        write_settings(settings)


def ask_for_export_path(settings, lb):
    settings["export_path"] = askdirectory(initialdir=settings['export_path'], 
                                           title='Selecione o Diretório de Destino')
    if settings['export_path']:
        lb["text"] = settings["export_path"]
        write_settings(settings)


def run_application(settings):
    
    # Validate export path
    if not export_path_is_valid(settings["export_path"]):
        return
    
    # Read the input file
    input_data = read_csv_file(settings["input_file"])
    if not input_data:
        return

    # Read the template file
    template_data = read_template_file(settings["template_file"])
    if not template_data:
        return

    # Write output files
    try:
        for data in input_data:
            output_data = generate_output_data(data, template_data)
            write_output_file(settings, output_data)
    except:
        messagebox.showerror('Erro', 'Não foi possível gerar os arquivos')
    else:
        messagebox.showinfo("Arquivos gerados", "Arquivos gerados com sucesso")


if path.exists("settings.json"):
    settings = load_settings()
else:
    # Gets the current path
    current_directory = path.dirname(path.abspath(__file__))

    settings = {
        'input_file': current_directory,
        'template_file': current_directory,
        'export_path': current_directory
    }

# Generate main window
root = Tk()

root.title("Gerador de Tags")

lbl_input = Label(root, text=settings["input_file"])
lbl_input.grid(row=0, column=1)

btn_input = Button(root, text="Arquivo de Entrada")
btn_input["command"] = partial(ask_for_input_file, settings, lbl_input)
btn_input.grid(row=0, column=0)

lbl_template = Label(root, text=settings["template_file"])
lbl_template.grid(row=1, column=1)

btn_template = Button(root, text="Arquivo de Modelo")
btn_template["command"] = partial(ask_for_template_file, settings, lbl_template)
btn_template.grid(row=1, column=0)

lbl_export_path = Label(root, text=settings["export_path"])
lbl_export_path.grid(row=2, column=1)

btn_export_path = Button(root, text="Caminho de Destino")
btn_export_path["command"] = partial(ask_for_export_path, settings, lbl_export_path)
btn_export_path.grid(row=2, column=0)

btn_run = Button(root, text="Gerar Arquivos")
btn_run["command"] = partial(run_application, settings)
btn_run.grid(row=3, column=0, columnspan=2)

root.mainloop()