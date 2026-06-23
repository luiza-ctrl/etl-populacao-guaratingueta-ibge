#testeteste

import pandas as pd
import sqlite3
import requests
import io

# 1. EXTRAIR - API IBGE Guaratinguetá código 3518403
print("Extraindo dados do IBGE...")
url = "https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/2000-2022/variaveis/9324?localidades=N6[3518403]"
dados = requests.get(url).json()

# 2. TRANSFORMAR - Pandas
lista = []
for ano, pop in dados[0]['resultados'][0]['series'][0]['serie'].items():
    if pop!= '-':
        lista.append({'ano': int(ano), 'populacao': int(pop)})

df = pd.DataFrame(lista)
df['crescimento_pct'] = df['populacao'].pct_change().round(2) * 100
df.to_csv('data/populacao_guaratingueta.csv', index=False)

# 3. LOAD - SQLite
conn = sqlite3.connect('database/populacao.db')
df.to_sql('populacao_guaratingueta', conn, if_exists='replace', index=False)
conn.close()
print("ETL concluído! Dados salvos em database/populacao.db")

