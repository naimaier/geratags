# coding: utf-8
import csv
from os import path
from tkinter import Tk, Frame, Label, Button, messagebox
from tkinter.filedialog import askopenfilename, askdirectory
from functools import partial
import json


class GeraTags():

    def __init__(self, root):
        # Try to load previously saved settings.
        try:
            self.settings = self.load_settings()    
        #  If unable or if not exists, load default settings
        except:
            # Gets the current path
            current_directory = path.dirname(path.abspath(__file__))

            self.settings = {
                'input_file': current_directory,
                'template_file': current_directory,
                'export_path': current_directory
            }

        """ GUI """
        self.root = root
        self.root.title("Gerador de Tags")
        self.root.resizable(width=False, height=False)

        self.main_frame = Frame(self.root, padx=10, pady=10)
        self.main_frame.pack(expand=True)

        self.lbl_title = Label(master=self.main_frame, 
                               font="Verdana 20 bold", 
                               padx=10, pady=10, 
                               text="Gerador de Tags\nTridium")
        self.lbl_title.grid(row=0, column=0)

        """ INPUT FRAME """
        self.input_frame = Frame(self.main_frame, padx=10, pady=10)
        self.input_frame.grid(row=1, column=0)

        self.lbl_input_title = Label(master=self.input_frame, 
                                     font="Verdana 14 bold", 
                                     text="Arquivo de Entrada (.csv)")
        self.lbl_input_title.pack()

        self.lbl_input = Label(master=self.input_frame, wraplength=250)
        self.lbl_input.pack()

        self.btn_input = Button(master=self.input_frame, text="Selecionar")
        self.btn_input["command"] = partial(self.ask_for_input_file)
        self.btn_input.pack()

        """ TEMPLATE FRAME """
        self.template_frame = Frame(self.main_frame, padx=10, pady=10)
        self.template_frame.grid(row=2, column=0)

        self.lbl_template_title = Label(master=self.template_frame, 
                                        font="Verdana 14 bold", 
                                        text="Arquivo de Modelo (.txt)")
        self.lbl_template_title.pack()

        self.lbl_template = Label(master=self.template_frame, wraplength=250)
        self.lbl_template.pack()

        self.btn_template = Button(master=self.template_frame, text="Selecionar")
        self.btn_template["command"] = partial(self.ask_for_template_file)
        self.btn_template.pack()

        """ EXPORT FRAME """
        self.export_frame = Frame(self.main_frame, padx=10, pady=10)
        self.export_frame.grid(row=3, column=0)

        self.lbl_export_title = Label(master=self.export_frame, 
                                      font="Verdana 14 bold", 
                                      text="Diretório de Destino")
        self.lbl_export_title.pack()

        self.lbl_export_path = Label(master=self.export_frame, wraplength=250)
        self.lbl_export_path.pack()

        self.btn_export_path = Button(master=self.export_frame, text="Selecionar")
        self.btn_export_path["command"] = partial(self.ask_for_export_path)
        self.btn_export_path.pack()

        """ RUN APP """
        self.btn_run = Button(self.main_frame, text="Gerar Arquivos")
        self.btn_run["command"] = partial(self.run_application)
        self.btn_run.grid(row=4, column=0, padx=10, pady=10)

        self.update_labels()


    def load_settings(self):
        settings = {}
        with open("settings.json", "r") as settings_file:
            settings = json.load(settings_file)

        return settings


    def write_settings_file(self):
        with open("settings.json", "w") as settings_file:
            json.dump(self.settings, settings_file)


    def read_csv_file(self):
        input_data = []

        # Read csv file (csv extension) into a dict list
        with open(self.settings['input_file'], 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                entry = {
                    "name": row[0],
                    "id": row[1]
                }
                input_data.append(entry)

        return input_data


    def read_template_file(self):
        template_data = []

        # Read template file (txt extension)
        with open(self.settings['template_file']) as template_file:
            template_data = template_file.readlines()

        return template_data


    def generate_output_data(self, input_data, template_data):
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


    def write_output_file(self, output_data):
        # Join the output file path and file name
        output_data['file_name'] = path.join(self.settings['export_path'], 
                                             output_data['file_name'])

        # Write file
        with open(output_data["file_name"] + ".mne", "w") as output_file:
            output_file.writelines(output_data["data"])


    def ask_for_input_file(self):
        input_file = askopenfilename(initialdir=self.settings['input_file'], 
                                     title='Selecione o Arquivo de Entrada', 
                                     filetypes=[('Arquivos CSV', '*.csv')])
        if input_file:
            self.settings['input_file'] = input_file
            self.update_labels()
            self.write_settings_file()


    def ask_for_template_file(self):
        template_file = askopenfilename(initialdir=self.settings['template_file'], 
                                        title='Selecione o Arquivo de Modelo', 
                                        filetypes=[('Arquivos TXT', '*.txt')])
        if template_file:
            self.settings['template_file'] = template_file
            self.update_labels()
            self.write_settings_file()


    def ask_for_export_path(self):
        export_path = askdirectory(initialdir=self.settings['export_path'], 
                                   title='Selecione o Diretório de Destino')
        if export_path:
            self.settings['export_path'] = export_path
            self.update_labels()
            self.write_settings_file()


    def update_labels(self):
        self.lbl_input['text'] = self.settings['input_file']
        self.lbl_template['text'] = self.settings['template_file']
        self.lbl_export_path['text'] = self.settings['export_path']


    def run_application(self):
        # Read the input file
        try:
            input_data = self.read_csv_file()
        except FileNotFoundError:
            messagebox.showerror('Erro', 'Arquivo inexistente: ' + self.settings["input_file"])
            return
        except:
            messagebox.showerror('Erro', 'Arquivo de entrada inválido: ' + self.settings["input_file"])
            return

        # Read the template file
        try:
            template_data = self.read_template_file()
        except FileNotFoundError:
            messagebox.showerror('Erro', 'Arquivo inexistente: ' + self.settings["template_file"])
            return
        except:
            messagebox.showerror('Erro', 'Arquivo de modelo inválido: ' + self.settings["template_file"])
            return

        # Write output files
        try:
            for data in input_data:
                output_data = self.generate_output_data(data, template_data)
                self.write_output_file(output_data)
        except FileNotFoundError:
            messagebox.showerror('Erro', 'Diretório de destino inválido')
            return
        except:
            messagebox.showerror('Erro', 'Não foi possível gerar os arquivos')
            return
        else:
            messagebox.showinfo("Informação", "Arquivos gerados com sucesso")
            return


# Generate main window
root = Tk()
gui = GeraTags(root)

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