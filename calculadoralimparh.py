import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
from tabulate import tabulate

# Funções de conversão
def converter_comprimento(valor):
    metro_cm = valor * 100
    return [
        ["De", "Para", "Resultado"],
        ["Metros", "Centímetros", f"{valor} m = {metro_cm:.2f} cm"]
    ]

def converter_peso(valor):
    kg_grama = valor * 1000
    return [
        ["De", "Para", "Resultado"],
        ["Quilograma", "Grama", f"{valor} kg = {kg_grama:.1f} g"]
    ]

def converter_temperatura(valor):
    celsius_fahr = (valor * 9/5) + 32
    return [
        ["De", "Para", "Resultado"],
        ["Celsius", "Fahrenheit", f"{valor} °C = {celsius_fahr:.1f} °F"]
    ]

# Função para atualizar a exibição com valores convertidos
def update_display():
    selected_type = type_var.get()
    value = float(entry_value.get())

    if selected_type == "Temperatura":
        converted_values = converter_temperatura(value)
    elif selected_type == "Comprimento":
        converted_values = converter_comprimento(value)
    elif selected_type == "Peso":
        converted_values = converter_peso(value)
    else:
        converted_values = []

    table_text = tabulate(converted_values, headers="firstrow", tablefmt="grid")
    text_display.config(state=tk.NORMAL)
    text_display.delete('1.0', tk.END)
    text_display.insert(tk.END, table_text)
    text_display.config(state=tk.DISABLED)

# Função para alterar a cor dos botões da calculadora
def change_button_color():
    colors = {
        "number": colorchooser.askcolor(title="Escolha a cor para botões de números")[1],
        "operator": colorchooser.askcolor(title="Escolha a cor para botões de operadores")[1],
        "equal": colorchooser.askcolor(title="Escolha a cor para o botão de igual")[1],
        "clear": colorchooser.askcolor(title="Escolha a cor para o botão de limpar")[1],
        "history": colorchooser.askcolor(title="Escolha a cor para o botão de limpar histórico")[1],
    }
    for button, (row, col) in buttons_calculator.items():
        if button == '=':
            btn = tk.Button(calculator_frame, text=button, width=10, command=calculate, fg="black", bg=colors["equal"], relief="sunken")
        elif button in {'/', '*', '-', '+'}:
            btn = tk.Button(calculator_frame, text=button, width=10, command=lambda btn=button: entry_calculator.insert(tk.END, btn),
                            fg="white", bg=colors["operator"], relief="sunken")
        elif button == 'C':
            btn = tk.Button(calculator_frame, text=button, width=10, command=lambda: entry_calculator.delete(0, tk.END),
                            fg="white", bg=colors["clear"], relief="sunken")
        elif button == 'T':
            btn = tk.Button(calculator_frame, text='limpar historico', width=11, command=clear_listbox, fg="white", bg=colors["history"],
                            relief="sunken")
        else:
            btn = tk.Button(calculator_frame, text=button, width=10, command=lambda btn=button: entry_calculator.insert(tk.END, btn),
                            fg="white", bg=colors["number"], relief="sunken")
        btn.grid(row=row, column=col, padx=5, pady=5)

# Função para adicionar item ao listbox
def add_to_list(item):
    my_list.append(item)
    update_listbox()

# Função para atualizar o listbox
def update_listbox():
    listbox.delete(0, tk.END)
    for item in my_list:
        listbox.insert(tk.END, item)

# Função para salvar histórico de cálculos em um arquivo
def save_calculation_to_txt(expression, result, file_name):
    try:
        with open(file_name, 'a') as file:
            file.write(expression + " = " + str(result) + '\n')
        print("Cálculos guardados no ficheiro:", file_name)
    except IOError:
        print("Erro: não foi possível guardar dados", file_name)

# Função para salvar lista em um arquivo
def save_list_to_txt(file_name, my_list):
    try:
        with open(file_name, 'w') as file:
            for item in my_list:
                file.write(str(item) + '\n')
        print("Ficheiro guardado:", file_name)
    except IOError:
        print("Erro", file_name)

# Função para limpar o listbox
def clear_listbox():
    my_list.clear()
    listbox.delete(0, tk.END)

# Função para lidar com o fechamento da janela
def on_closing():
    save_list_to_txt(file_name, my_list)
    window.destroy()

# Função para calcular a expressão na calculadora
def calculate():
    expression = entry_calculator.get()
    try:
        result = eval(expression)
        entry_calculator.delete(0, tk.END)
        entry_calculator.insert(tk.END, f"{result:.3f}")
        save_calculation_to_txt(expression, f"{result:.3f}", calculation_file_name)
        add_to_list(expression + " = " + f"{result:.3f}")
    except Exception as e:
        entry_calculator.delete(0, tk.END)
        entry_calculator.insert(tk.END, "")
        messagebox.showerror("Erro", "Expressão inválida")
        entry_calculator.delete(0, tk.END)

# Função para lidar com eventos de pressionamento de tecla
def key_press(event):
    if event.keysym == "Return":
        calculate()
    elif event.widget == entry_calculator:
        return
    else:
        key = event.char
        if key in "0123456789+-*/.":
            button_click(key)
        elif key == "c" or key == "C":
            if entry_calculator != window.focus_get() and not entry_calculator.get():
                clear()

# Função para adicionar dígitos à entrada da calculadora
def button_click(value):
    entry_calculator.insert(tk.END, value)

# Janela principal do Tkinter
window = tk.Tk()
window.title("Conversão de Unidades & Calculadora com Histórico")

# Criação do notebook para abas
notebook = ttk.Notebook(window)
notebook.pack(pady=10, expand=True)

# Frame para o conversor de unidades
converter_frame = tk.Frame(notebook)
converter_frame.pack(fill="both", expand=True)

# Frame para a calculadora
calculator_frame = tk.Frame(notebook)
calculator_frame.pack(fill="both", expand=True)

# Frame para configurações
settings_frame = tk.Frame(notebook)
settings_frame.pack(fill="both", expand=True)

# Adicionar abas ao notebook
notebook.add(calculator_frame, text="Calculadora")

notebook.add(converter_frame, text="Conversor")

notebook.add(settings_frame, text="Configurações")

# Configuração da aba do conversor de unidades
type_var = tk.StringVar()
measure_types = ["Temperatura", "Comprimento", "Peso"]
type_label = tk.Label(converter_frame, text="Selecione o tipo de medida:")
type_combobox = ttk.Combobox(converter_frame, textvariable=type_var, values=measure_types, state="readonly")
type_combobox.current(0)  # Selecionar o primeiro tipo de medida por padrão
entry_value = ttk.Entry(converter_frame)
convert_button = ttk.Button(converter_frame, text="Converter", command=update_display)
text_display = tk.Text(converter_frame, height=10, width=50)
text_display.config(state=tk.DISABLED)

# Layout da aba do conversor de unidades
type_label.grid(row=0, column=0, padx=10, pady=10)
type_combobox.grid(row=0, column=1, padx=10, pady=10)
entry_value.grid(row=1, column=0, columnspan=2, pady=5)
convert_button.grid(row=2, column=0, columnspan=2, pady=5)
text_display.grid(row=3, column=0, columnspan=2, pady=5)

# Configuração da aba da calculadora
entry_calculator = tk.Entry(calculator_frame, font=("Arial", 18), justify="right")
entry_calculator.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

buttons_calculator = {
    '7': (1, 0), '8': (1, 1), '9': (1, 2), '/': (1, 3),
    '4': (2, 0), '5': (2, 1), '6': (2, 2), '*': (2, 3),
    '1': (3, 0), '2': (3, 1), '3': (3, 2), '-': (3, 3),
    'C': (4, 0), '0': (4, 1), '=': (4, 2), '+': (4, 3),
    'T': (5, 0), '.': (5, 1)
}

# Layout dos botões da calculadora
for button, (row, col) in buttons_calculator.items():
    if button == '=':
        btn = tk.Button(calculator_frame, text=button, width=10, command=calculate, fg="black", bg="yellow", relief="sunken")
    elif button in {'/', '*', '-', '+'}:
        btn = tk.Button(calculator_frame, text=button, width=10, command=lambda btn=button: entry_calculator.insert(tk.END, btn),
                        fg="white", bg="green", relief="sunken")
    elif button == 'C':
        btn = tk.Button(calculator_frame, text=button, width=10, command=lambda: entry_calculator.delete(0, tk.END),
                        fg="white", bg="red", relief="sunken")
    elif button == 'T':
        btn = tk.Button(calculator_frame, text='limpar historico', width=11, command=clear_listbox, fg="white", bg="red", relief="sunken")
    else:
        btn = tk.Button(calculator_frame, text=button, width=10, command=lambda btn=button: entry_calculator.insert(tk.END, btn),
                        fg="white", bg="blue", relief="sunken")
    btn.grid(row=row, column=col, padx=5, pady=5)

# Criação e posicionamento do listbox do histórico
history_label = tk.Label(calculator_frame, text="Histórico dos cálculos", font=("Arial", 12, "bold"))
history_label.grid(row=6, column=0, columnspan=4, pady=10)

listbox = tk.Listbox(calculator_frame, width=40, height=10)
listbox.grid(row=7, column=0, columnspan=4, pady=10, padx=10)

# Lista e nomes dos arquivos para salvar os dados
my_list = []
file_name = "calculations2.txt"
calculation_file_name = "calculations.txt"

# Carregar lista existente do arquivo
try:
    with open(file_name, 'r') as file:
        my_list = file.read().splitlines()
except FileNotFoundError:
    pass

update_listbox()

# Configuração da aba de configurações
settings_label = tk.Label(settings_frame, text="Configurações de cores", font=("Arial", 12, "bold"))
settings_label.pack(pady=10)

change_color_button = ttk.Button(settings_frame, text="Mudar cores dos botões", command=change_button_color)
change_color_button.pack(pady=10)

# Vinculação de eventos
window.bind("<Key>", key_press)
window.protocol("WM_DELETE_WINDOW", on_closing)

# Iniciar a interface gráfica
window.mainloop()
