"""# Importando as Bibliotecas"""
import pandas as pd
import time
import sys
import os

"""# Configuração do Web-Driver"""
# Utilizando o WebDriver do Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Se receber os argumentos via linha de comando, atribui os argumentos as variáveis
if len(sys.argv) > 1:
    pais = sys.argv[1]
    liga = sys.argv[2]
    link = sys.argv[3]

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

# next dict
next = {
    'Div':[],
    'Date':[],
    'Time':[],
    'HomeTeam':[],
    'AwayTeam':[]
}

# Coleta de dados
table = wd_Chrome.find_element(By.CSS_SELECTOR, 'table.stats_table')
rows  = table.find_elements(By.CSS_SELECTOR, 'tr')
for row in rows:
    try:
        score = row.find_element(By.CSS_SELECTOR, 'td[ data-stat="score"]').text
        if not score.strip():
            home  = row.find_element(By.CSS_SELECTOR, 'td[ data-stat="home_team"]').text
            if home:
                away  = row.find_element(By.CSS_SELECTOR, 'td[ data-stat="away_team"]').text
                date  = row.find_element(By.CSS_SELECTOR, 'td[ data-stat="date"]').get_attribute('csk')
                # start = row.find_element(By.CSS_SELECTOR, 'td[ data-stat="start_time"]').get_attribute('csk')
                start = row.find_element(By.CSS_SELECTOR, 'td[ data-stat="start_time"] span.localtime').text.strip("()")
                next['Div'].append(liga)
                next['Date'].append(date)
                next['Time'].append(start)
                next['HomeTeam'].append(home)
                next['AwayTeam'].append(away)
                print(f'{liga} {date} {start} {home} x {away}')
    except Exception as error:
        # print(f'Erro: {error}')
        pass

# # Salvar no CSV
df = pd.DataFrame(next)
df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
df['DATETIME'] = pd.to_datetime(df['Date'].dt.strftime('%Y-%m-%d') + ' ' + df['Time'])
filename = "data/all_next.csv"

if os.path.exists(filename):
    df_antigo = pd.read_csv(filename, sep=";")
    df_antigo['DATETIME'] = pd.to_datetime(df_antigo['Date'] + ' ' + df_antigo['Time'], format='%d/%m/%Y %H:%M')
    df_total = pd.concat([df_antigo, df], ignore_index=True)
    df_total.drop_duplicates(keep='last', inplace=True)
else:
    df_total = df

df_total = df_total.sort_values(by='DATETIME')
df_total['Date'] = df_total['DATETIME'].dt.strftime('%d/%m/%Y')
df_total['Time'] = df_total['DATETIME'].dt.strftime('%H:%M')
df_total = df_total.drop(columns=['DATETIME'])
df_total.reset_index(drop=True, inplace=True)
df_total.index = df_total.index.set_names(['Nº'])
df_total = df_total.rename(index=lambda x: x + 1)
df_total.to_csv(filename, sep=";", index=False)
