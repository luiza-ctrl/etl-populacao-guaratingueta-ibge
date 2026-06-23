import pandas as pd
import sqlite3
import requests
import os

# 1. EXTRAIR - API IBGE Guaratinguetá código 3518404
print("Extraindo dados do IBGE...")
url = (
    "https://servicodados.ibge.gov.br/api/v3/agregados/6579/"
    "periodos/2000-2022/variaveis/9324?localidades=N6[3518404]"
)

response = requests.get(url)
response.raise_for_status()

dados = response.json()

# 2. TRANSFORMAR - Pandas
lista = []
serie = dados[0]['resultados'][0]['series'][0]['serie']

for ano, pop in serie.items():
    if pop != '-':
        lista.append({'ano': int(ano), 'populacao': int(pop)})

df = pd.DataFrame(lista)
df['crescimento_pct'] = df['populacao'].pct_change().round(2) * 100
df.to_csv('data/populacao_guaratingueta.csv', index=False)

# 3. LOAD - SQLite
os.makedirs('database', exist_ok=True)
if os.path.exists('database/populacao.db'):
    os.remove('database/populacao.db')

conn = sqlite3.connect('database/populacao.db')
df.to_sql('populacao_guaratingueta', conn, if_exists='replace', index=False)
conn.close()

print("ETL concluído! Dados salvos em database/populacao.db")