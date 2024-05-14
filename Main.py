# 2° Importação das Bibliotecas
import matplotlib.pyplot as plt  # Biblioteca para plotagem de gráficos
import geopandas as gpd  # Biblioteca para manipulação de dados geoespaciais
from shapely.geometry import Point, LineString  # Biblioteca para geometrias espaciais
import pandas as pd  # Biblioteca para manipulação de dados tabulares
import numpy as np  # Biblioteca para manipulação de arrays e operações matemáticas

# 3° Definição da Função calcular_direcao
def calcular_direcao(x, y):
    # Calcula a direção (derivada) ao longo de uma trajetória definida por coordenadas x e y
    dx = np.gradient(x)
    dy = np.gradient(y)
    return dx, dy

# 4° Coleta de Informações dos Satélites
num_satelites = int(input("Digite o número de satélites: "))  # Número de satélites a serem rastreados
dados_satelites = []  # Lista para armazenar dados dos satélites
cores = ['red', 'blue', 'green', 'yellow', 'purple', 'orange']  # Lista de cores para cada satélite

for i in range(num_satelites):
    nome = input(f"Digite o nome do satélite {i+1}: ")  # Nome do satélite
    trajetoria = input(f"Digite a trajetória do satélite {i+1} (formato: x1,y1;x2,y2;...): ")  # Trajetória do satélite
    local_atual = input(f"Digite a localização atual do satélite {i+1} (formato: x,y): ")  # Localização atual do satélite
    
    # Processamento da trajetória
    pontos = [tuple(map(float, p.split(','))) for p in trajetoria.split(';')]  # Convertendo trajetória em lista de pontos
    
    # Obtendo a localização atual
    local_atual = tuple(map(float, local_atual.split(',')))  # Convertendo localização atual em tupla de coordenadas
    
    # Criando a entrada de dados do satélite
    dados_satelites.append({
        'nome': nome,
        'trajetoria': LineString(pontos),
        'local_atual': Point(local_atual),
        'cor': cores[i % len(cores)]
    })

# 5° Criação do DataFrame com os dados dos satélites
df = pd.DataFrame(dados_satelites)  # Criando DataFrame com os dados dos satélites

# 6° Carregamento do Mapa do Mundo
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))  # Carregando mapa do mundo

# 7° Plotagem das Trajetórias e Locais Atuais
fig, ax = plt.subplots(1, 1, figsize=(15, 10))  # Criando figura e eixo para o gráfico
world.plot(ax=ax, color='white', edgecolor='black')  # Plotando o mapa do mundo

for _, row in df.iterrows():
    trajetoria = row['trajetoria']  # Obtendo a trajetória do satélite atual
    x, y = trajetoria.xy  # Extraindo coordenadas x e y da trajetória
    dx, dy = calcular_direcao(x, y)  # Calculando a direção ao longo da trajetória
    
    # Plotar trajetória
    ax.plot(x, y, label=row['nome'], color=row['cor'], linewidth=0.5)  # Plotando a trajetória
    
    # Calculando o comprimento máximo para normalizar o tamanho das setas
    comprimento_max = np.sqrt(dx[-1]**2 + dy[-1]**2)
    if comprimento_max > 0:
        dx_norm = dx[-1] / comprimento_max
        dy_norm = dy[-1] / comprimento_max
    else:
        dx_norm, dy_norm = 0, 0

    # Plotando a direção com seta de tamanho fixo
    ax.quiver(x[-1:], y[-1:], dx_norm, dy_norm, scale=20, color=row['cor'], width=0.005, headlength=5, headwidth=3)  # Plotando a direção
    
    # Plotando o local atual
    ax.plot(row['local_atual'].x, row['local_atual'].y, 'o', color='black')  # Plotando o local atual como ponto

plt.legend()  # Adicionando legenda ao gráfico
plt.show()  # Exibindo o gráfico
