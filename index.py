"""# Importando as Bibliotecas"""
import pandas as pd
import time
from tqdm import tqdm
from datetime import datetime, timedelta
import pytz
import re
import sys
import os
import numpy as np

"""# Configuração do Web-Driver"""
# Utilizando o WebDriver do Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# Escolha da campeonato
ligas = {
    "chile" : "https://fbref.com/en/comps/35/schedule/Chilean-Primera-Division-Scores-and-Fixtures",
    "colombia" : "https://fbref.com/en/comps/41/schedule/Primera-A-Scores-and-Fixtures",
    "dinamarca" : "https://fbref.com/en/comps/50/schedule/Danish-Superliga-Scores-and-Fixtures",
    "inglaterra" : "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures",
    "italia" : "https://fbref.com/en/comps/11/schedule/Serie-A-Scores-and-Fixtures",
    "espanha" : "https://fbref.com/en/comps/12/schedule/La-Liga-Scores-and-Fixtures",
    "alemanha" : "https://fbref.com/en/comps/20/schedule/Bundesliga-Scores-and-Fixtures",
    "frança" : "https://fbref.com/en/comps/13/schedule/Ligue-1-Scores-and-Fixtures"
}

if len(sys.argv) > 1:
    pais = sys.argv[1]
    if pais in ligas:
        print(f'{pais} encontrado.')
    else:
        print(f'{pais} não encontrado.')
        sys.exit(1)
# pais = 'chile'
link = ligas.get(pais, 'https://fbref.com/en')

# Instanciando o Objeto ChromeOptions
options = webdriver.ChromeOptions()

# Passando algumas opções para esse ChromeOptions
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--start-maximized')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-crash-reporter')
options.add_argument('--log-level=3')
options.add_argument('--disable-gpu')
options.add_argument('--enable-unsafe-swiftshader')

# Criação do WebDriver do Chrome
wd_Chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

"""# Iniciando a Raspagem de Dados"""

# Com o WebDrive a gente consegue a pedir a página (URL)
wd_Chrome.get(link) 
time.sleep(2)
# wd_Chrome.save_screenshot('screen.png')

# data dict
dados = {
    'WEEK':[],
    'DATE':[],
    'HOME':[],
    'AWAY':[],
    'FTHG':[],
    'FTAG':[],
    'DIFF':[]
}

next = {
    'WEEK':[],
    'DATE':[],
    'HOME':[],
    'AWAY':[]
}

# Coleta de dados
table = wd_Chrome.find_element(By.CSS_SELECTOR, 'table.stats_table')
rows  = table.find_elements(By.CSS_SELECTOR, 'tr')
for row in rows:
    try:
        week  = row.find_element(By.CSS_SELECTOR, 'th[ data-stat="gameweek"]').text
        date  = row.find_element(By.CSS_SELECTOR, 'td[ data-stat="date"]').get_attribute('csk')
        home  = row.find_element(By.CSS_SELECTOR, 'td[ data-stat="home_team"]').text
        away  = row.find_element(By.CSS_SELECTOR, 'td[ data-stat="away_team"]').text
        score = row.find_element(By.CSS_SELECTOR, 'td[ data-stat="score"]').text
        if not score.strip():
            if home:
                # print(f'{home} x {away}')
                next['WEEK'].append(week)
                next['DATE'].append(date)
                next['HOME'].append(home)
                next['AWAY'].append(away)
        else:
            fthg  = score.split('–')[0]
            ftag  = score.split('–')[1]
            diff  = int(fthg) - int(ftag)
            dados['WEEK'].append(week)
            dados['DATE'].append(date)   
            dados['HOME'].append(home)
            dados['AWAY'].append(away)
            dados['FTHG'].append(fthg)
            dados['FTAG'].append(ftag)
            dados['DIFF'].append(diff)
            # print(f'{home} {fthg} x {ftag} {away}')
    except Exception as error:
        # print(f'Erro: {error}')
        pass

# Iterando pelas chaves e imprimindo o tamanho de cada lista
# for key, value in dados.items():
#     print(f'Tamanho de {key}: {len(value)}')
# for key, value in next.items():
#     print(f'Tamanho de {key}: {len(value)}')

# # Salvar no CSV
df = pd.DataFrame(dados)
# Convertendo a coluna 'DATE' para datetime e formatando para 'dd/mm/yyyy'
df['DATE'] = pd.to_datetime(df['DATE'], format='%Y%m%d')
df['DATE'] = df['DATE'].dt.strftime('%d/%m/%Y')
df.reset_index(inplace=True, drop=True)
df.index = df.index.set_names(['Nº'])
df = df.rename(index=lambda x: x + 1)
filename = f"data/{pais}.csv"
df.to_csv(filename, sep=";", index=False)

# # Salvar no CSV
# Seleciona as 10 primeiras entradas de cada lista usando fatiamento
week_subset = next['WEEK'][:10]
date_subset = next['DATE'][:10]
home_subset = next['HOME'][:10]
away_subset = next['AWAY'][:10]
df = pd.DataFrame({'WEEK': week_subset, 'DATE': date_subset, 'HOME': home_subset, 'AWAY': away_subset})
# Convertendo a coluna 'DATE' para datetime e formatando para 'dd/mm/yyyy'
df['DATE'] = pd.to_datetime(df['DATE'], format='%Y%m%d')
df['DATE'] = df['DATE'].dt.strftime('%d/%m/%Y')
#df = pd.DataFrame(next) #todos os jogos
df.reset_index(inplace=True, drop=True)
df.index = df.index.set_names(['Nº'])
df = df.rename(index=lambda x: x + 1)
filename = f"data/{pais}_next.csv"
df.to_csv(filename, sep=";", index=False)