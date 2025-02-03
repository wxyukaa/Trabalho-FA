# Análise: O objetivo do código é processar o arquivo medals.csv e gerar 2 tabelas. Uma das tabelas apresenta de forma decrescente os países que mais obtiveram
#          medalhas de ouro, prata e bronze, apresentadno em sua última coluna o número total de medalhas adquiridas. A segunda tabela apresenta quais países receberam
#          apenas, e somente, medalhas de um único gênero competitivo.
#          Foi utilizado somente 2 tipos estruturados para a construção do código. A primeira delas **DadosOlimpicos** foi utilizada para filtragem de informações
#          mais importante do arquivo csv. O segundo tipo **CountryCounting** foi utilizada para gerar um estruturado que armazena os tipos de medalhas, país e generos.
# 
# Entrada de dados: depende unicamente do arquivo csv **medals.csv** -- O arquivo precisou ser alterado em algumas linhas específicas para que pudesse fazer a
#                   geração de lista de tipos estruturados **tabelas_dados**.
#
# Tipos de dados utilizados: matrizes, classes de estruturas, listas de estuturas, conversão de str para int.
#
# Alterações feitas no medals.csv:
# linha 471 com código da medalha vazio, foi alterado para 3.
# As linhas finais do arquivo estavam com o código da medalha em float, foi alterado para int manualmente.
# Alguma linha perdida entre 700 a 900 que possuia a modalidade como 10,000 ao inves de 10.000 também foi alterado para não gerar problemas para lidar com os índices
#
# Saída de dados: O código devolve duas listas de estruturas: quadro de medalhas ordenada, quadro de países que receberam medalhas apenas no gênero feminino e
#                 paises que receberam medalhas apenas no gênero masculino

import sys

def le_arquivo(nome: str) -> list[list[str]]:
    '''
    Lê o conteúdo do arquivo *nome* e devolve uma lista onde cada elemento é
    uma lista com os valores das colunas de uma linha (valores separados por
    vírgula). A primeira linha do arquivo, que deve conter o nome das
    colunas, é descartado.
    Por exemplo, se o conteúdo do arquivo for
    tipo,cor,ano
    carro,verde,2010
    moto,branca,1995
    a resposta produzida é
    [['carro', 'verde', '2010'], ['moto', 'branca', '1995']]
    '''
    try:
        with open(nome) as f:
            tabela = []
            linhas = f.readlines()
        for i in range(1, len(linhas)):
            tabela.append(linhas[i].split(','))
        return tabela
    except IOError as e:
        print(f'Erro na leitura do arquivo "{nome}": {e.errno} - {e.strerror}.');
        sys.exit(1)

from dataclasses import dataclass

@dataclass
class DadosOlimpicos: #estrutura feita para converter a matriz em lista de estruturas, tendo os países repetidos
    cod_medalha: int
    cod_pais: str
    gender : str

@dataclass
class CountryCounting: #utilizda para converter a lista de estruturas para outra, retirando as repetições e somando o número de cada campo
    country: str
    gold: int
    silver: int
    bronze: int
    total: int
    mulheres: int
    homens: int

@dataclass
class GeneroFem:
    country: str
    mulheres: int

@dataclass
class GeneroMasc:
    country: str
    homens: int

def converte_dados(tabela: list[list[str]]) -> list[DadosOlimpicos]:
    r'''
    filtra os dados mais importantes do arquivo de medalhas e converte a lista de strings em lista de DadosOlimpicos
    
    Exemplos:
    >>> converte_dados([['Gold Medal','1','2024-07-27','Remco EVENEPOEL','M','Cycling Road','Men's Individual Time Trial','ATH','/en/paris-2024/results/cycling-road/men-s-individual-time-trial/fnl-000100--','1903136','BEL','Belgium','Belgium'], ['Silver Medal','2','2024-07-27','Filippo GANNA','M','Cycling Road','Men's Individual Time Trial','ATH','/en/paris-2024/results/cycling-road/men-s-individual-time-trial/fnl-000100--','1923520','ITA','Italy','Italy']])
    [DadosOlimpicos(cod_medalha=1, cod_pais='BEL', gender='M'), DadosOlimpicos(cod_medalha=2, cod_pais='ITA', gender='M')]

    >>> converte_dados([['Silver Medal','2','2024-07-27','Anna HENDERSON','W','Cycling Road','Women's Individual Time Trial','ATH','/en/paris-2024/results/cycling-road/women-s-individual-time-trial/fnl-000100--','1912525','GBR','Great Britain','Great Britain'],
['Bronze Medal','3','2024-07-27','Chloe DYGERT','W','Cycling Road','Women's Individual Time Trial','ATH','/en/paris-2024/results/cycling-road/women-s-individual-time-trial/fnl-000100--','1955079','USA','United States','United States of America'],
['Gold Medal','1','2024-07-27','China','W','Diving','Women's Synchronised 3m Springboard','TEAM','/en/paris-2024/results/diving/women-s-synchronised-3m-springboard/fnl-000100--','DIVW3MTEAM2-CHN01','CHN','China','People's Republic of China']])
    [DadosOlimpicos(cod_medalha=2, cod_pais='GBR', gender='W'), DadosOlimpicos(cod_medalha=3, cod_pais='USA', gender='W'), DadosOlimpicos(cod_medalha=1, cod_pais='CHN', gender='W')]
    
    >>> converte_dados([['Gold Medal','1','2024-07-27','Remco EVENEPOEL','M','Cycling Road','Men's Individual Time Trial','ATH','/en/paris-2024/results/cycling-road/men-s-individual-time-trial/fnl-000100--','1903136','BEL','Belgium','Belgium'],
['Silver Medal','2','2024-07-27','Filippo GANNA','M','Cycling Road','Men's Individual Time Trial','ATH','/en/paris-2024/results/cycling-road/men-s-individual-time-trial/fnl-000100--','1923520','ITA','Italy','Italy'],
['Bronze Medal','3','2024-07-27','Wout van AERT','M','Cycling Road','Men's Individual Time Trial','ATH','/en/paris-2024/results/cycling-road/men-s-individual-time-trial/fnl-000100--','1903147','BEL','Belgium','Belgium'],
['Gold Medal','1','2024-07-27','Grace BROWN','W','Cycling Road','Women's Individual Time Trial','ATH','/en/paris-2024/results/cycling-road/women-s-individual-time-trial/fnl-000100--','1940173','AUS','Australia','Australia'],
['Silver Medal','2','2024-07-27','Anna HENDERSON','W','Cycling Road','Women's Individual Time Trial','ATH','/en/paris-2024/results/cycling-road/women-s-individual-time-trial/fnl-000100--','1912525','GBR','Great Britain','Great Britain'],
['Bronze Medal','3','2024-07-27','Chloe DYGERT','W','Cycling Road','Women's Individual Time Trial','ATH','/en/paris-2024/results/cycling-road/women-s-individual-time-trial/fnl-000100--','1955079','USA','United States','United States of America'],
['Gold Medal','1','2024-07-27','China','W','Diving','Women's Synchronised 3m Springboard','TEAM','/en/paris-2024/results/diving/women-s-synchronised-3m-springboard/fnl-000100--','DIVW3MTEAM2-CHN01','CHN','China','People's Republic of China']])
    [DadosOlimpicos(cod_medalha=1, cod_pais='BEL', gender='M'), DadosOlimpicos(cod_medalha=2, cod_pais='ITA', gender='M'), DadosOlimpicos(cod_medalha=3, cod_pais='BEL', gender='M'), DadosOlimpicos(cod_medalha=1, cod_pais='AUS', gender='W'), DadosOlimpicos(cod_medalha=2, cod_pais='GBR', gender='W'), DadosOlimpicos(cod_medalha=3, cod_pais='USA', gender='W'), DadosOlimpicos(cod_medalha=1, cod_pais='CHN', gender='W')]
    '''
    tabela_dados = []
    for olimpiadas in tabela:
        cod_medalha = int(olimpiadas[1])
        cod_pais = olimpiadas[10]
        genero = olimpiadas[4]
        tabela_dados.append(DadosOlimpicos(cod_medalha, cod_pais, genero))
    return tabela_dados

def listagem_paises(tabela_dados: list[DadosOlimpicos]) -> list:
    '''
    cria uma lista de de str de todos os países que receberam medalhas, sem haver reptição.

    Exemplos:
    >>> listagem_paises([DadosOlimpicos(cod_medalha=1, cod_pais='BEL', gender='M'), DadosOlimpicos(cod_medalha=2, cod_pais='ITA', gender='M'), DadosOlimpicos(cod_medalha=3, cod_pais='BEL', gender='M'), DadosOlimpicos(cod_medalha=1, cod_pais='AUS', gender='W'), DadosOlimpicos(cod_medalha=2, cod_pais='GBR', gender='W'), DadosOlimpicos(cod_medalha=3, cod_pais='USA', gender='W'), DadosOlimpicos(cod_medalha=1, cod_pais='CHN', gender='W')])
    ['BEL', 'ITA', 'AUS', 'GBR', 'USA', 'CHN']

    >>> listagem_paises([DadosOlimpicos(cod_medalha=3, cod_pais='USA', gender='W'), DadosOlimpicos(cod_medalha=1, cod_pais='CHN', gender='W')])
    ['USA', 'CHN']

    >>> listagem_paises([DadosOlimpicos(cod_medalha=1, cod_pais='BEL', gender='M'), DadosOlimpicos(cod_medalha=2, cod_pais='ITA', gender='M'), DadosOlimpicos(cod_medalha=3, cod_pais='BEL', gender='M'), DadosOlimpicos(cod_medalha=1, cod_pais='AUS', gender='W')])
    ['BEL', 'ITA', 'AUS']
    '''
    lista_paises = []
    for dados in tabela_dados:
        if dados.cod_pais not in lista_paises:
            lista_paises.append(dados.cod_pais)
    return lista_paises

def quadro_de_medalhas(tabela_dados: list[DadosOlimpicos], lista_paises: list[str]) -> list:
    r'''
    Utilizando a lista_paises e a tabela_dados como parâmetro, foi feita uma nova nova lista de tipo CountryCounting onde foi armazenado a sigla do país, o número de cada tipo de medalha obtido e
    de que tipo de gênero cada medalha foi adquirida. 

    Exemplos:
    >>> quadro_de_medalhas([DadosOlimpicos(cod_medalha=1, cod_pais='BEL', gender='M'), DadosOlimpicos(cod_medalha=2, cod_pais='ITA', gender='M'), DadosOlimpicos(cod_medalha=3, cod_pais='BEL', gender='M'), DadosOlimpicos(cod_medalha=1, cod_pais='AUS', gender='W'), DadosOlimpicos(cod_medalha=2, cod_pais='GBR', gender='W'), DadosOlimpicos(cod_medalha=3, cod_pais='USA', gender='W'), DadosOlimpicos(cod_medalha=1, cod_pais='CHN', gender='W')])      
    [CountryCounting(country='BEL', gold=1, silver=0, bronze=1, total=2, mulheres=0, homens=2), CountryCounting(country='AUS', gold=1, silver=0, bronze=0, total=1, mulheres=1, homens=0), CountryCounting(country='CHN', gold=1, silver=0, bronze=0, total=1, mulheres=1, homens=0), CountryCounting(country='GBR', gold=0, silver=1, bronze=0, total=1, mulheres=1, homens=0), CountryCounting(country='USA', gold=0, silver=0, bronze=1, total=1, mulheres=1, homens=0), CountryCounting(country='ITA', gold=0, silver=1, bronze=0, total=1, mulheres=0, homens=1)]

    >>> quadro_de_medalhas([DadosOlimpicos(cod_medalha=1, cod_pais='BRA', gender='W')])
    [CountryCounting(country='BRA', gold=1, silver=0, bronze=0, total=1, mulheres=1, homens=0)]

    >>> quadro_de_medalhas([DadosOlimpicos(cod_medalha=1, cod_pais='BRA', gender='W')], [DadosOlimpicos(cod_medalha=1, cod_pais='BRA', gender='W')], [DadosOlimpicos(cod_medalha=1, cod_pais='BRA', gender='W')])
    [CountryCounting(country='BRA', gold=3, silver=0, bronze=0, total=3, mulheres=3, homens=0)]
    '''
    quadro_medalhas = []
    for pais in lista_paises:
        ouro = 0
        prata = 0
        bronze = 0
        mulheres = 0
        homens = 0
        for dados in tabela_dados:
            if dados.cod_pais == pais:
                if dados.cod_medalha == 1:
                    ouro = ouro + 1
                elif dados.cod_medalha == 2:
                    prata = prata + 1
                elif dados.cod_medalha == 3:
                    bronze = bronze + 1
                if dados.gender == "W":
                    mulheres = mulheres + 1
                if dados.gender == "M":
                    homens = homens + 1
        total = ouro + prata + bronze
        aux = CountryCounting(pais, ouro, prata, bronze, total, mulheres, homens)
        quadro_medalhas.append(aux)
    return quadro_medalhas

def ordena_quadro(quadro_medalhas:list[CountryCounting]) -> list[CountryCounting]:
    r'''
    Ordena a lista quadro_medalhas pela quantidade de medalhas e tem ordem de prioridade: ouro > prata > bronze

    Exemplo:
    >>> ordena_quadro([CountryCounting(country='BEL', gold=1, silver=0, bronze=1, total=2, mulheres=0, homens=2), CountryCounting(country='AUS', gold=1, silver=0, bronze=0, total=1, mulheres=1, homens=0), CountryCounting(country='CHN', gold=1, silver=0, bronze=0, total=1, mulheres=1, homens=0), CountryCounting(country='GBR', gold=0, silver=1, bronze=0, total=1, mulheres=1, homens=0), CountryCounting(country='USA', gold=0, silver=0, bronze=1, total=1, mulheres=1, homens=0), CountryCounting(country='ITA', gold=0, silver=1, bronze=0, total=1, mulheres=0, homens=1)])
    [CountryCounting(country='BEL', gold=1, silver=0, bronze=1, total=2, mulheres=0, homens=2), CountryCounting(country='AUS', gold=1, silver=0, bronze=0, total=1, mulheres=1, homens=0), CountryCounting(country='CHN', gold=1, silver=0, bronze=0, total=1, mulheres=1, homens=0), CountryCounting(country='GBR', gold=0, silver=1, bronze=0, total=1, mulheres=1, homens=0), CountryCounting(country='USA', gold=0, silver=0, bronze=1, total=1, mulheres=1, homens=0), CountryCounting(country='ITA', gold=0, silver=1, bronze=0, total=1, mulheres=0, homens=1)]

    >>> ordena_quadro([CountryCounting(country='BRA', gold=3, silver=0, bronze=0, total=3, mulheres=3, homens=0), CountryCounting(country='EUA', gold=15, silver=20, bronze=7, total=42, mulheres=10, homens=9), CountryCounting(country='AUS', gold=15, silver=10, bronze=3, total=28, mulheres=7, homens=9), CountryCounting(country='ITA', gold=8, silver=20, bronze=6, total=34, mulheres=8, homens=10)])
    [CountryCounting(country='EUA', gold=15, silver=20, bronze=7, total=42, mulheres=10, homens=9), CountryCounting(country='AUS', gold=15, silver=10, bronze=3, total=28, mulheres=7, homens=9), CountryCounting(country='ITA', gold=8, silver=20, bronze=6, total=34, mulheres=8, homens=10), CountryCounting(country='BRA', gold=3, silver=0, bronze=0, total=3, mulheres=3, homens=0)]
    '''
    for i in range(len(quadro_medalhas)):
        for j in range(i + 1, len(quadro_medalhas)):
            if quadro_medalhas[j].gold > quadro_medalhas[i].gold:
                imax = quadro_medalhas[j]
                quadro_medalhas[j] = quadro_medalhas[i]
                quadro_medalhas[i] = imax
            elif quadro_medalhas[j].gold == quadro_medalhas[i]:
                if quadro_medalhas[j].silver > quadro_medalhas[i].silver:
                    aux = quadro_medalhas[j]
                    quadro_medalhas[j] = quadro_medalhas[i]
                    quadro_medalhas[i] = aux
                elif quadro_medalhas[j].silver == quadro_medalhas[i].silver:
                    x = quadro_medalhas[j]
                    quadro_medalhas[j] = quadro_medalhas[i]
                    quadro_medalhas[i] = x
    return quadro_medalhas      
        
def imprime_quadro(quadro_medalhas: list[CountryCounting]):
    print('PAÍS', '   ', 'OURO', ' ', 'PRATA', 'BRONZE', ' ', 'TOTAL')
    for i in range(len(quadro_medalhas)):
        print(quadro_medalhas[i].country, '     ', quadro_medalhas[i].gold, '   ', quadro_medalhas[i].silver,  '   ', quadro_medalhas[i].bronze, '   ', quadro_medalhas[i].total)
    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def separa_feminino(quadro_medalhas: list[CountryCounting]) -> list[GeneroFem]:
    list_woman = []
    if quadro_medalhas == []:
        return list_woman
    else:
        if quadro_medalhas[0].mulheres > 0 and quadro_medalhas[0].homens == 0:
            aux = GeneroFem(quadro_medalhas[0].country, quadro_medalhas[0].mulheres)
            list_woman.append(aux)
            list_woman = list_woman + separa_feminino(quadro_medalhas[1:])
        else:
            list_woman = separa_feminino(quadro_medalhas[1:])
    return list_woman
    
def separa_masculino(quadro_medalhas: list[CountryCounting]) -> list[GeneroMasc]:
    list_man = []
    if quadro_medalhas == []:
        return list_man
    else:
        if quadro_medalhas[0].mulheres == 0 and quadro_medalhas[0].homens > 0:
            aux = GeneroMasc(quadro_medalhas[0].country, quadro_medalhas[0].homens)
            list_man.append(aux)
            list_man = list_man + separa_masculino(quadro_medalhas[1:])
        else:
            list_man = separa_masculino(quadro_medalhas[1:])
    return list_man

def imprime_generos(list_woman: list[GeneroFem], list_man: list[GeneroMasc]):
    print('Lista de países medalhistas somente no gênero feminino:')
    print('PAÍS', 'QTDE DE MEDALHAS')
    for i in range(len(list_woman)):
        print(list_woman[i].country, list_woman[i].mulheres)
    print('\n')
    print('Lista de países medalhistas somente no gênero masculino:')
    print('PAÍS', 'QTDE DE MEDALHAS')
    for i in range(len(list_man)):
        print(list_man[i].country, list_man[i].homens)
        
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def main():
    if len(sys.argv) < 2:
        print('Nenhum nome de arquivo informado.')
        sys.exit(1)
    if len(sys.argv) > 2:
        print('Muitos parâmetro. Informe apenas um nome de arquivo.')
        sys.exit(1)
    tabela = le_arquivo(sys.argv[1])
    lista_tabela = converte_dados(tabela) #converte a matriz em lista de estruturado DadosOlimpicos
    paises = listagem_paises(lista_tabela) #faz uma listagem de paises, é uma lista de strings
    quadro = quadro_de_medalhas(lista_tabela, paises) #faz uma lista de estruturas com a contagem de cada tipo de medalha e a contagem de medalhas no genero feminino e masculino
    quadro_organizado = ordena_quadro(quadro) #apenas reordena a lista quadro_medalhas

    print(imprime_quadro(quadro_organizado))
    print('\n')

    femininos = separa_feminino(quadro) #filtra os países femininos
    masculinos = separa_masculino(quadro) #filtra os países masculinos
    print(imprime_generos(femininos, masculinos))


if __name__ == '__main__':
    main()
