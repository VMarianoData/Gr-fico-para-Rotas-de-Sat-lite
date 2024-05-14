# 2° Importação das Bibliotecas

import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point, LineString
import pandas as pd
import numpy as np

# 3° Definição da Função calcular_direcao
def calcular_direcao(x, y):
    dx = np.gradient(x)
    dy = np.gradient(y)
    return dx, dy

# 4° Coleta de Informações dos Satélites
num_satelites = int(input("Digite o número de satélites: "))
dados_satelites = []
cores = ['red', 'blue', 'green', 'yellow', 'purple', 'orange']

for i in range(num_satelites):
    nome = input(f"Digite o nome do satélite {i+1}: ")
    trajetoria = input(f"Digite a trajetória do satélite {i+1} (formato: x1,y1;x2,y2;...): ")
    local_atual = input(f"Digite a localização atual do satélite {i+1} (formato: x,y): ")
    pontos = [tuple(map(float, p.split(','))) for p in trajetoria.split(';')]
    local_atual = tuple(map(float, local_atual.split(',')))
    dados_satelites.append({'nome': nome, 'trajetoria': LineString(pontos), 'local_atual': Point(local_atual), 'cor': cores[i % len(cores)]})

# 5° Criação do DataFrame
df = pd.DataFrame(dados_satelites)

# 6° Carregamento do Mapa do Mundo
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# 7° Plotagem das Trajetórias e Locais Atuais
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
world.plot(ax=ax, color='white', edgecolor='black')

for _, row in df.iterrows():
    trajetoria = row['trajetoria']
    x, y = trajetoria.xy
    dx, dy = calcular_direcao(x, y)
   
    # Plotar trajetória
    ax.plot(x[:-1], y[:-1], label=row['nome'], color=row['cor'], linewidth=0.5)
   
    # Plotar direção
    ax.quiver(x[-1:], y[-1:], dx[-1:], dy[-1:], scale_units='xy', angles='xy', scale=1, color=row['cor'], width=0.005, headlength=3, headwidth=1.5, headaxislength=2.25) 

    # Plotar local atual
    ax.plot(row['local_atual'].x, row['local_atual'].y, 'o', color='black')  

plt.legend()
plt.show()
