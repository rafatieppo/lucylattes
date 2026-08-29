import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from lucyLattes import run_lucyLattes
import resources

root = tk.Tk()
root.title('lucyLattes')
root.geometry('700x360')

# colors
cbg_conf = '#dfe318'
cbg_config = '#22a884'
cbg_run = '#2a788e'
cbg_quit = '#440154'
cfw_quit = '#FFFFFF'

# logo
img = PhotoImage(file='./fig_lucy.png')
# canvas = tk.Canvas(root, width=120, height=120)
# canvas.grid(row=0, column=0, padx=0, pady=0, rowspan=2)
# canvas.create_image(0, 8, anchor='nw', image=img)
lab_log = tk.Label(root, image=img)
lab_log.grid(row=0, column=0, padx=0, pady=0, sticky='w')

lab_00 = tk.Label(root, width=50, padx=0, pady=0, anchor='e',
                  text='Para saber mais: \
                  \n https://github.com/rafatieppo/lucylattes \
                  \nrafaeltieppo@yahoo.com.br')
lab_00.grid(row=0, column=1, padx=0)

lab01 = tk.Label(root, bg=cbg_conf, text="Configuracoes",
                 relief=tk.RIDGE, width=85)
lab01.grid(row=6, column=0, pady=3, sticky="w", columnspan=2)

# ano inicial
lab_yi = tk.Label(root,
                  text="Digite ano Inicial para tabulacao de dados:",
                  anchor='w')
lab_yi.grid(row=9, column=0)
var_yi = tk.IntVar()
var_yi.set(2010)
e_yi = tk.Entry(root, textvariable=var_yi)
e_yi.grid(row=9, column=1, sticky="W")

# ano final
lab_yf = tk.Label(root, text='Digite ano Final para tabulacao de dados:')
lab_yf.grid(row=10, column=0)
var_yf = tk.IntVar()
var_yf.set(2020)
e_yf = tk.Entry(root, textvariable=var_yf)
e_yf.grid(row=10, column=1, sticky='W')

# qualis
lsjcr_qls = resources.read_jcr_qls('./jcr_qualis/lsqualis.txt')
lab_qls = tk.Label(root, text='Escolha o arquivo qualis:')
lab_qls.grid(row=11, column=0)
combo = ttk.Combobox(root,
                     state='readonly',
                     values=lsjcr_qls, width=45)
combo.grid(row=11, column=1, sticky='W')
var_qls = combo.get()

lab_pg = tk.Label(root,
                  text='Digite o Nome do PG: ')
lab_pg.grid(row=13, column=0)
var_pg = tk.StringVar()
var_pg.set('Ambiente e Sistemas de Produção Agrícola')
e_pg = tk.Entry(root, textvariable=var_pg, width=50)
e_pg.grid(row=13, column=1, sticky="W")

# Checkbox
# Create label frame
checkGroup = tk.LabelFrame(root, text="Options", padx=10, pady=10)
checkGroup.grid(row=16, column=0, sticky="W")
var_rm_csv = tk.IntVar()
c1 = tk.Checkbutton(checkGroup, text='Apagar csv de csv_producao',
                    variable=var_rm_csv, onvalue=1, offvalue=0)
c1.grid(row=20, column=0, padx=0)

# Run indicadors capes
var_indcapes = 0

# Run hwesci
var_hwebsci = 0

# write txt config file


def set_configs_tk():
    'Mostra as configs em uma tela de mensagem.'
    var_qls = combo.get()
    if var_qls == '':
        tk.messagebox.showwarning(title='Atencao',
                                  message='Qualis nao selecionado')
    else:
        ls_descrip = ['ano inicial:', 'ano final:', 'qualis:',
                      'pg:', 'apagar csv_producao:',
                      'calcular indcapes:', 'calcular hwebsci:']
        ls_configs = [str(var_yi.get()), str(var_yf.get()),
                      str(var_qls.rstrip()), str(var_pg.get()),
                      str(var_rm_csv.get()),
                      str(var_indcapes), str(var_hwebsci)]
        msg_vars = str(
            'Confirme as configuracoes: \
            \nAno inicial:{} \
            \nAno final: {} \
            \nQualis:\n {} \
            \nPG: {} \
            \nRemover Csv (0 Nao 1 Sim): {}'.format(
                var_yi.get(), var_yf.get(), var_qls.rstrip(),
                var_pg.get(), var_rm_csv.get()))
        tk.messagebox.showinfo(message=msg_vars,
                               title='Confirme:')
        with open('./config_tk.txt', 'w', encoding='UTF-8') as f:
            for idz in range(len(ls_configs)):
                f.write(ls_descrip[idz] + ls_configs[idz] + '\n')
            f.close()
        return ls_configs


# button
b1 = tk.Button(root, text="Run LucyLattes",
               command=run_lucyLattes,
               bg=cbg_run)
b1.grid(row=21, column=1, padx=25, sticky='E')
b2 = tk.Button(root, text="Gravar configuracoes",
               command=set_configs_tk,
               bg=cbg_config)
b2.grid(row=21, column=1, padx=25, sticky='W')
b3 = tk.Button(root, text="Quit",
               # command=root.destroy,
               command=exit,
               bg=cbg_quit, foreground=cfw_quit)
b3.grid(row=22, column=1, padx=25, sticky='E')

root.mainloop()
