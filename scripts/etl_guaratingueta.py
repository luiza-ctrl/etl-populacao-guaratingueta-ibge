#testeteste

import pandas as pd
import sqlite3
import requests
import io

# 1. EXTRAIR - API IBGE Guaratinguetá código 3518403
print("Extraindo dados do IBGE...")
url = "https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/2000-2022/variaveis/9324?localidades=N6[3518403]"
dados = requests.get(url).json()
