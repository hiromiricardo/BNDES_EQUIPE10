# Imports necessário
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# configurações dos plots e pandas
plt.rc('ytick', labelsize=8)            # define os tamanhos das letras do eixo y como 8
plt.rc('xtick', labelsize=8)            # define os tamanhos das letras do eixo y como 8
plt.rc('axes', titlesize=10)            # define o tamanho da letra do título como 10
plt.rcParams.update({'figure.autolayout': True})         # define o tamanho do grafico como autolayout para se adaptar ao tamanho da área de exibição
pd.options.display.float_format = '{:.2f}'.format       # define o formato dos floats


# Criação da classe Desembolso
class Desembolso:

    def __init__(self):
        # ao instanciar a classe, abre o arquivo desembolsos-mensais como DataFrame(DF)
        # cabe aqui mudar o caminho
        self.df = pd.read_csv(r'desembolsos-mensais.csv', sep=";", decimal=",", encoding="UTF-8")

    def get_regiao(self):
        # metodo para obter a região do dataFrame (DF)
        df1 = self.df['regiao'].value_counts()  # pega os valores que estão contidos na coluna regiao do DF
        df1 = dict(df1)  # transforma em um dicionario
        regioes = []
        for i in df1.keys():  # percorre o dicionario pegando apenas as chaves
            regioes.append(i)  # adiciona na lista regioes
        return sorted(regioes)  # retorna a lista

    def get_estado(self):
        # metodo para obter os estados do DF
        df1 = self.df['uf'].value_counts()  # pega os valores que estão contidos na coluna uf do DF
        aux = dict(df1)  # transforma em um dicionario
        estados = []
        for i in aux.keys():  # percorre o dicionario pegando apenas as chaves
            estados.append(i)  # adiciona na lista estados
        return sorted(estados)  # retorna a lista

    def get_municipio(self, estado):
        # metodo para obter os municipios
        dic = self.df.loc[self.df['uf'] == estado]  # filtra o DF de acordo com o estado passado como argumento
        aux = dic['municipio'].value_counts()  # pega os valores que estão contidos na coluna municipio do DF
        aux = dict(aux)  # transforma em um dicionario
        municipios = []
        for i in aux.keys():  # percorre o dicionario pegando apenas as chaves
            municipios.append(i)  # adiciona na lista municipios
        return sorted(municipios)  # retorna a lista

    def get_ano(self, ref, local):
        # metodo para obter o ano
        dic = self.df.loc[self.df[ref] == local]  # filtra o DF pelo local passado como argumento
        aux = dic['ano'].value_counts()  # pega os valores que estão contidos na coluna municipio do DF
        aux = dict(aux)  # transforma em um dicionario
        ano = []
        for i in aux.keys():  # percorre o dicionario pegando apenas as chaves
            ano.append(i)
        return sorted(ano)  # retorna a lista

    def plot_regiao(self, nome, anoini, anofin):
        # metodo para plotar gráfico referente a região, dado um intervalo pelos anos
        desembolso = self.df.loc[(self.df['ano'] >= anoini) & (self.df['ano'] <= anofin)]  # filtra o DF pelos anos
        desembolso = desembolso.groupby(by=['regiao', 'ano']).sum('desembolsos_reais')  # agrupa o DF pela regiao e
        # ano, somando o desembolso
        aux = desembolso.loc[[nome]]  # localiza o nome da regiao
        desembolso_reg = aux.xs(nome, level=0, axis=0, drop_level=True)  # drop_level
        desembolso_reg = desembolso_reg.drop(columns=['mes', 'municipio_codigo'])   # dropa as colunas mes e
        # municioio-codigo
        plt.close()
        # plot gráfico
        grafico = plt.figure(figsize=(15, 6))
        plt.title(f'Desembolso do BNDES para a região {nome}')
        plt.xticks(rotation=90)
        sns.pointplot(x=desembolso_reg.index, y=desembolso_reg['desembolsos_reais'])
        plt.grid()
        return grafico

    def plot_estado(self, nome, anoini, anofin):
        # método para plotar grafico referente ao estado, dado um intervalo de ano
        # segue a mesma logica do método anterior
        # filtragem e agrupamento do DF
        desembolso = self.df.loc[(self.df['ano'] >= anoini) & (self.df['ano'] <= anofin)]
        desembolso = desembolso.groupby(by=['uf', 'ano']).sum('desembolsos_reais')
        aux = desembolso.loc[[nome]]
        desembolso_est = aux.xs(nome, level=0, axis=0, drop_level=True)
        desembolso_est = desembolso_est.drop(columns=['mes', 'municipio_codigo'])
        plt.close()
        #plot grafico
        grafico = plt.figure(figsize=(15, 6))
        plt.title(f'Desembolso do BNDES para o Estado de {nome}')
        plt.xticks(rotation=90)
        sns.pointplot(x=desembolso_est.index, y=desembolso_est['desembolsos_reais'])
        plt.grid()
        return grafico

    def plot_municipio(self, nome, anoini, anofin):
        # método para plotar grafico referente ao municipio, dado um intervalo de ano
        # segue a mesma logica do método anterior
        # filtragem e agrupamento do DF
        desembolso = self.df.loc[(self.df['ano'] >= anoini) & (self.df['ano'] <= anofin)]
        desembolso = desembolso.groupby(by=['municipio', 'ano']).sum('desembolsos_reais')
        aux = desembolso.loc[[nome]]
        desembolso_mun = aux.xs(nome, level=0, axis=0, drop_level=True)
        desembolso_mun = desembolso_mun.drop(columns=['mes', 'municipio_codigo'])
        plt.close()
        # plot grafico
        grafico = plt.figure(figsize=(15, 6))
        plt.title(f'Desembolso do BNDES para a cidade de {nome}')
        plt.xticks(rotation=90)
        sns.pointplot(x=desembolso_mun.index, y=desembolso_mun['desembolsos_reais'])
        plt.grid()
        return grafico  # para testar a fução, substituir o return por plt.show()

    def plot_subsetor_regiao(self, nome, anoini, anofin):
        # método para plotar grafico referente ao subsetor da regiao, dado um intervalo de ano
        # Filtragem do DF pelo intervalo de ano
        subsetor = self.df.loc[(self.df['ano'] >= anoini) & (self.df['ano'] <= anofin)]
        plt.close()
        # plot grafico
        grafico = plt.figure(figsize=(21, 11))
        plt.title(f'Valor de desembolso do BNDES por subsetor no período de {anoini} a {anofin} na região {nome}')
        # filtragem pelo nome da regiao
        data = subsetor.loc[subsetor['regiao'] == nome]
        sns.barplot(y=data['subsetor_bndes'], x=data['desembolsos_reais'])
        return grafico

    def plot_subsetor_estado(self, nome, anoini, anofin):
        # método para plotar grafico referente ao subsetor do estado, dado um intervalo de ano
        # Filtragem do DF pelo intervalo de ano
        subsetor = self.df.loc[(self.df['ano'] >= anoini) & (self.df['ano'] <= anofin)]
        plt.close()
        # plot grafico
        grafico = plt.figure(figsize=(15, 10))
        plt.title(f'Valor de desembolso do BNDES por subsetor no período de {anoini} a {anofin} no estado de {nome}')
        # filtragem pelo nome do estado
        data = subsetor.loc[subsetor['uf'] == nome]
        sns.barplot(y=data['subsetor_bndes'], x=data['desembolsos_reais'])
        return grafico

    def plot_subsetor_municipio(self, nome, anoini, anofin):
        # método para plotar grafico referente ao subsetor do municipio, dado um intervalo de ano
        # Filtragem do DF pelo intervalo de ano
        subsetor = self.df.loc[(self.df['ano'] >= anoini) & (self.df['ano'] <= anofin)]
        plt.close()
        # plot grafico
        grafico = plt.figure(figsize=(15, 10))
        plt.title(f'Valor de desembolso do BNDES por subsetor no período de {anoini} a {anofin} da cidade de {nome}')
        # filtragem pelo nome do munucipio
        data = subsetor.loc[subsetor['municipio'] == nome]
        sns.barplot(y=data['subsetor_bndes'], x=data['desembolsos_reais'])
        return grafico
