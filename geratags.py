# coding: utf-8
import csv
from os import path
from tkinter import Tk, Frame, Label, Button, messagebox
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


def read_csv_file(input_file_name):
    input_data = []

    # Read csv file (csv extension) into a dict list
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
    
    # Read the input file
    try:
        input_data = read_csv_file(settings["input_file"])
    except FileNotFoundError:
        messagebox.showerror('Erro', 'Arquivo inexistente: ' + settings["input_file"])
        return
    except:
        messagebox.showerror('Erro', 'Não foi possível abrir o arquivo de entrada: ' + settings["input_file"])
        return

    # Read the template file
    try:
        template_data = read_template_file(settings["template_file"])
    except FileNotFoundError:
        messagebox.showerror('Erro', 'Arquivo inexistente: ' + settings["template_file"])
        return

    except:
        messagebox.showerror('Erro', 'Não foi possível abrir o arquivo de modelo: ' + settings["template_file"])
        return

    # Write output files
    try:
        for data in input_data:
            output_data = generate_output_data(data, template_data)
            write_output_file(settings, output_data)
    except FileNotFoundError:
        messagebox.showerror('Erro', 'Diretório de destino inválido')
    except:
        messagebox.showerror('Erro', 'Não foi possível gerar os arquivos')
    else:
        messagebox.showinfo("Informação", "Arquivos gerados com sucesso")


# Try to load previously saved settings.
try:
    settings = load_settings()
    
#  If unable or if not exists, load default settings
except:
    # Gets the current path
    current_directory = path.dirname(path.abspath(__file__))

    settings = {
        'input_file': current_directory,
        'template_file': current_directory,
        'export_path': current_directory
    }

""" GUI """
# Generate main window
root = Tk()
root.title("Gerador de Tags")
root.resizable(width=False, height=False)

main_frame = Frame(root, padx=10, pady=10)
main_frame.pack(expand=True)

lbl_title = Label(master=main_frame, font="Verdana 20 bold", padx=10, pady=10, text="Gerador de Tags\nTridium")
lbl_title.grid(row=0, column=0)

""" INPUT FRAME """
input_frame = Frame(main_frame, padx=10, pady=10)
input_frame.grid(row=1, column=0)

lbl_input_title = Label(master=input_frame, font="Verdana 14 bold", text="Arquivo de Entrada (.csv)")
lbl_input_title.pack()

lbl_input = Label(master=input_frame, wraplength=250, text=settings["input_file"])
lbl_input.pack()

btn_input = Button(master=input_frame, text="Selecionar")
btn_input["command"] = partial(ask_for_input_file, settings, lbl_input)
btn_input.pack()

""" TEMPLATE FRAME """
template_frame = Frame(main_frame, padx=10, pady=10)
template_frame.grid(row=2, column=0)

lbl_template_title = Label(master=template_frame, font="Verdana 14 bold", text="Arquivo de Modelo (.txt)")
lbl_template_title.pack()

lbl_template = Label(master=template_frame, wraplength=250, text=settings["template_file"])
lbl_template.pack()

btn_template = Button(master=template_frame, text="Selecionar")
btn_template["command"] = partial(ask_for_template_file, settings, lbl_template)
btn_template.pack()

""" EXPORT FRAME """
export_frame = Frame(main_frame, padx=10, pady=10)
export_frame.grid(row=3, column=0)

lbl_export_title = Label(master=export_frame, font="Verdana 14 bold", text="Diretório de Destino")
lbl_export_title.pack()

lbl_export_path = Label(master=export_frame, wraplength=250, text=settings["export_path"])
lbl_export_path.pack()

btn_export_path = Button(master=export_frame, text="Selecionar")
btn_export_path["command"] = partial(ask_for_export_path, settings, lbl_export_path)
btn_export_path.pack()

""" RUN APP """
btn_run = Button(main_frame, text="Gerar Arquivos")
btn_run["command"] = partial(run_application, settings)
btn_run.grid(row=4, column=0, padx=10, pady=10)

# Necessary for winfo_width and winfo_heigh to work properly
root.update()

""" Centering the window on the screen """
# https://yagisanatode.com/2018/02/24/how-to-center-the-main-window-on-the-screen-in-tkinter-with-python-3/
# Changed winfo_reqwidth and winfo_reqheight to winfo_width and winfo_height

# Gets the requested values of the height and widht.
windowWidth = root.winfo_width() 
windowHeight = root.winfo_height()
 
# Gets both half the screen width/height and window width/height
positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
 
# Positions the window in the center of the page.
root.geometry("+{}+{}".format(positionRight, positionDown))

root.mainloop()