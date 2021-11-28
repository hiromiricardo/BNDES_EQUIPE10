import tkinter as tk  # módulo tkinter para criar a GUI
from tkinter import ttk  # importa o ttk dentro do tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # módulo para plotar os gráficos
from Desembolso_Mensal import Desembolso  # arquivo onde faz as buscas na base de dados

# Criando a janela utilizando o Tkinter
window = tk.Tk()  # Iniciando o Tkinter
window.title('Hackathon BNDES')  # Colacando o titulo
windowWidth = 1280  # Largura da página
windowHeight = 600  # Altura da página
sw = window.winfo_screenwidth()  # Obtendo a largura da tela do usuário
sh = window.winfo_screenheight()  # Obtendo a altura da tela do usuário
x = (sw / 2) - (windowWidth / 2)  # Calculo para identificar o centro da tela (horizontal)
y = (sh / 2) - (windowHeight / 2)  # Calculo para identificar o centro da tela (vertical)
window.geometry(f'{windowWidth}x{windowHeight}+{int(x)}+{int(y)}')  # Setando o tamanho da janela e a
# posição de abertura
dbm = Desembolso()  # Iniciando a classe Desembolso para buscar as funções e apresentá-las

# label text do titulo
ttk.Label(window, text="HACKATHON BNDES", foreground="green",  # label do titulo e posicionando no centro
          font=("Times New Roman", 15, 'bold')).place(x=(windowWidth / 2), y=15, anchor='center')

# Criando os frames e definindo as posições
fm_search = tk.LabelFrame(window, text="Pesquisa", padx=10, pady=10)  # Criando o LabelFrame da parte de pesquisa
fm_search.place(x=15, y=30, height=490, width=310)  # Definindo a posição do LabelFrame de pesquisa

fm_result = tk.LabelFrame(window, text="Resultados", padx=10, pady=10)  # Criando o LabelFrame da parte de aprentação
fm_result.place(x=340, y=30, height=490, width=920)  # Definindo a posição do LabelFrame de apresentação


# Função para criar os botões de salvar os plots e alterar entre eles
def create_buttons():
    global button_change, list_graphs, save_button  # Definindo as variaveis como global
    if len(list_graphs) == 1:  # Compara se é apenas um ou mais gráficos
        button_change = tk.Button(window, text='gráfico por subsetor', state='disabled',
                                  # Botão para alterar o gráfico apresentado iniciando em estado desabilitado
                                  height=1, width=20).place(x=790, y=545, anchor='center')
        save_button = tk.Button(window, text='Salvar gráfico', command=lambda: save_plot(),
                                # Botão para salvar o gráfico apresentado
                                ).place(x=1250, y=545, anchor='e')
    else:  # se for mais de um gráfico
        button_change = tk.Button(window, text='gráfico por subsetor', command=lambda: change_plot(1),
                                  # Botão para alterar o gráfico apresentado iniciando em estado habilitado
                                  height=1, width=20).place(x=790, y=545, anchor='center')
        save_button = tk.Button(window, text='Salvar gráfico', command=lambda: save_plot()
                                ).place(x=1250, y=545, anchor='e')


# função para salvar os gráficos apresentados
def save_plot():
    from tkinter.filedialog import askdirectory  # importação do módulo para perguntar o diretorio
    global list_graphs, int_save  # variaveis globais
    int_save += 1  # para diferenciar o nome e não sobrepor
    path = askdirectory()  # pergunta o diretorio para salvar
    list_graphs[0].savefig(path + '/gráfico ' + str(int_save) + '.png')  # salva o gráfico no diretorio informado
    if len(list_graphs) == 2:  # caso tenha mais de um gráfico, salva os dois
        list_graphs[1].savefig(path + '/Subplot ' + str(int_save) + '.png')


# Função para alterar o gráfico exibido na tela
def change_plot(pos):
    global button_change, save_button
    plot_graph(pos)
    if pos == 1:  # para definir se esta no primeiro gráfico ou no segundo
        button_change = tk.Button(window, text='gráfico por região', command=lambda: change_plot(0),
                                  # altera a função do botão
                                  height=1, width=20).place(x=790, y=545, anchor='center')
        save_button = tk.Button(window, text='Salvar gráfico', command=lambda: save_plot()).place(x=1250, y=545,
                                                                                                  # redefina o botão salvar
                                                                                                  anchor='e')
    else:
        button_change = tk.Button(window, text='gráfico por subsetor', command=lambda: change_plot(1),
                                  # altera a função do botão
                                  height=1, width=20).place(x=790, y=545, anchor='center')
        save_button = tk.Button(window, text='Salvar gráfico', command=lambda: save_plot(),  # redefina o botão salvar
                                ).place(x=1250, y=545, anchor='e')


# Função que cria o label e o combobox
def lab_comb(frame, pos, text):
    ttk.Label(frame, text=text, font=("Times New Roman", 12)).grid(row=pos, padx=20,
                                                                   pady=0)  # definindo a letra e a posição
    var = tk.StringVar()
    combo_box = ttk.Combobox(frame, width=35, textvariable=var,
                             state="readonly")  # cria o combobox na função apenas leitura
    combo_box.grid(row=(pos + 1), padx=20, pady=5)  # define a posição do combobox
    combo_box.current()
    return combo_box


# Função para limpar o gráfico apresentado (para poder alterar entre os gráficos)
def clear_graph():
    global list_graphs, canvas
    try:  # caso não tenha gráfico para limpar, não dar erro
        list_graphs.clear()  # limpa a lista de gráficos
        canvas.get_tk_widget().destroy()  # destroy a tela exibida
    except:
        pass


# função para exibir o gráfico na tela
def plot_graph(pos):
    global canvas
    try:
        canvas.get_tk_widget().destroy()  # na hora de alterar entre os gráficos, limpa a tela
    except:
        pass
    create_buttons()  # chamada da função de criar os botões
    canvas = FigureCanvasTkAgg(list_graphs[pos], fm_result)  # passa a figura para o canvas
    canvas.draw()
    canvas.get_tk_widget().pack(fill='x')  # define a posição do canvas


# Radio Button para a opção de exibir o gráfico por subsetor
def radio_button():
    ttk.Label(fm_search, text="Deseja visualizar os gráficos por subsetor tambem?"  # label do texto
              ).place(x=145, y=380, anchor='center')
    boolean_var = tk.BooleanVar()  # recebe a variável
    option_no = tk.Radiobutton(fm_search, text="Não", variable=boolean_var, value=False)  # opção 'não'
    option_yes = tk.Radiobutton(fm_search, text="Sim", variable=boolean_var, value=True)  # opção 'sim'
    option_no.place(x=140, y=395, anchor='ne')  # posição da opção 'não'
    option_yes.place(x=150, y=395, anchor='nw')  # posição da opção 'sim'
    return boolean_var


# Função para escolha da categoria
def choose_category(event):
    value = event.widget.get()
    fm_choose = tk.LabelFrame(fm_search, text="Dados da busca desejada", padx=10, pady=10)
    fm_choose.place(x=0, y=60, height=300, width=290)
    subsetor_bool = radio_button()

    # de acordo com a busca os labels e combobox de opção são apresentados na tela
    if value == 'Busca por Região':
        region = lab_comb(fm_choose, 1,
                          "Selecione a região de busca:")  # chama a função de criar as labes+combobox e define os valores e posição
        region['value'] = tuple(dbm.get_regiao())  # define os valores da combobox buscando no Desembolso_Mensal.py
        year_start = lab_comb(fm_choose, 3, "Selecione o ano inicial:")
        year_start.configure(width=15)  # define um tamanho menor do que o padrão da função
        year_end = lab_comb(fm_choose, 5, "Selecione o ano final:")
        year_end.configure(width=15)

        def year_value(event):  # função para buscar os anos disponiveis para a região selecionada
            st = event.widget.get()  # recebe a variável do combobox anterior selecionado
            years = tuple(dbm.get_ano('regiao', st))  # recebe os anos disponiveis buscando no Desembolso_Mensal.py
            year_start['value'] = years  # atibui o valor ao combobox do ano inicial
            year_end['value'] = years  # atribui o valor ao combobox do ano final
            year_start.current(0)  # define para pre-selecionar o ultimo ano disponível
            year_end.current(len(years) - 1)  # define para pre-selecionar o ultimo ano disponível

        region.bind("<<ComboboxSelected>>", year_value)

        def region_plot():  # plota o(s) gráfico(s) da região selecionada
            global list_graphs
            if not subsetor_bool.get():  # confere se vai plotar por subsetor
                global plot
                plot = dbm.plot_regiao(region.get(), int(year_start.get()),
                                       int(year_end.get()))  # busca o gráfico no Desembolso_Mensal.py
                list_graphs = [plot]  # define a lista de gráficos
                pass
            else:  # se sim
                global plot_1, plot_2
                plot_1 = dbm.plot_regiao(region.get(), int(year_start.get()),
                                         int(year_end.get()))  # busca o gráfico no Desembolso_Mensal.py
                plot_2 = dbm.plot_subsetor_regiao(region.get(), int(year_start.get()),
                                                  int(year_end.get()))  # busca o gráfico no Desembolso_Mensal.py
                clear_graph()  # chamada da função de limpar
                list_graphs = [plot_1, plot_2]  # define a lista de gráficos
                pass
            plot_graph(0)
            pass

        plot_button = ttk.Button(fm_search, text='Gerar gráficos', command=region_plot)  # define a função do botão
        plot_button.place(x=145, y=440, anchor='center')

    elif value == 'Busca por Estado':
        state = lab_comb(fm_choose, 1, "Selecione o estado de busca:")
        state['value'] = tuple(dbm.get_estado())
        year_start = lab_comb(fm_choose, 5, "Selecione o ano inicial:")
        year_start.configure(width=15)
        year_end = lab_comb(fm_choose, 7, "Selecione o ano final:")
        year_end.configure(width=15)

        def year_value(event):  # função para buscar os anos disponiveis para o estado selecionado
            st = event.widget.get()
            years = tuple(dbm.get_ano('uf', st))
            year_start['value'] = years
            year_end['value'] = years
            year_start.current(0)
            year_end.current(len(years) - 1)

        state.bind("<<ComboboxSelected>>", year_value)

        def state_plot():  # plota o(s) gráfico(s) do estado selecionado
            global list_graphs
            if not subsetor_bool.get():
                global plot
                plot = dbm.plot_estado(state.get(), int(year_start.get()), int(year_end.get()))
                list_graphs = [plot]
                pass
            else:
                global plot_1, plot_2
                plot_1 = dbm.plot_estado(state.get(), int(year_start.get()), int(year_end.get()))
                plot_2 = dbm.plot_subsetor_estado(state.get(), int(year_start.get()), int(year_end.get()))
                clear_graph()
                list_graphs = [plot_1, plot_2]
                pass
            plot_graph(0)
            pass

        plot_button = ttk.Button(fm_search, text='Gerar gráficos', command=state_plot)
        plot_button.place(x=145, y=440, anchor='center')

    elif value == 'Busca por Município':
        state = lab_comb(fm_choose, 1, "Selecione o estado:")
        state['value'] = tuple(dbm.get_estado())
        city = lab_comb(fm_choose, 3, "Selecione o Município de busca:")
        year_start = lab_comb(fm_choose, 5, "Selecione o ano inicial:")
        year_start.configure(width=15)
        year_end = lab_comb(fm_choose, 7, "Selecione o ano final:")
        year_end.configure(width=15)

        def city_values(event):  # função para buscar as cidades disponiveis para o estado selecionado
            st = event.widget.get()
            city['value'] = tuple(dbm.get_municipio(st))

        def year_value(event):  # função para buscar os anos disponiveis para cidade selecionada
            st = event.widget.get()
            years = tuple(dbm.get_ano('municipio', st))
            year_start['value'] = years
            year_end['value'] = years
            year_start.current(0)
            year_end.current(len(years) - 1)

        state.bind("<<ComboboxSelected>>", city_values)
        city.bind("<<ComboboxSelected>>", year_value)

        def city_plot():  # plota o(s) gráfico(s) da cidade selecionada
            global list_graphs
            if not subsetor_bool.get():
                global plot
                plot = dbm.plot_municipio(city.get(), int(year_start.get()), int(year_end.get()))
                list_graphs = [plot]
                pass
            else:
                global plot_1, plot_2
                plot_1 = dbm.plot_municipio(city.get(), int(year_start.get()), int(year_end.get()))
                plot_2 = dbm.plot_subsetor_municipio(city.get(), int(year_start.get()), int(year_end.get()))
                clear_graph()
                list_graphs = [plot_1, plot_2]
                pass
            plot_graph(0)
            pass

        plot_button = ttk.Button(fm_search, text='Gerar gráficos', command=city_plot)
        plot_button.place(x=145, y=440, anchor='center')


# inicia a tela com essa combobox
int_save = 0  # inicia a variável como 0 (essa variável é para diferenciar o nome na hora de salvar
selection = lab_comb(fm_search, 1, "Selecione a busca desejada")  # cria label de seleção da opção
selection['values'] = ('Busca por Região',  # define os valores da combobox
                       'Busca por Estado',
                       'Busca por Município')
selection.bind("<<ComboboxSelected>>",
               choose_category)  # função 'bind' faz com que quando escolher uma opção ela execute uma função especifica

window.mainloop()  # para a tela permanecer aberta até o usuário decidir fecha-la
