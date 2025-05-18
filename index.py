"""# Importando as Bibliotecas"""
import pandas as pd
import time
import sys

"""# Configuração do Web-Driver"""
# Utilizando o WebDriver do Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Recebe os argumentos via linha de comando
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

# # Salvar no CSV
df = pd.DataFrame(dados)
# Convertendo a coluna 'DATE' para datetime e formatando para 'dd/mm/yyyy'
df['DATE'] = pd.to_datetime(df['DATE'], format='%Y%m%d')
df['DATE'] = df['DATE'].dt.strftime('%d/%m/%Y')
df.reset_index(inplace=True, drop=True)
df.index = df.index.set_names(['Nº'])
df = df.rename(index=lambda x: x + 1)
filename = f"data/{pais}-{liga}.csv"
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
filename = f"data/{pais}-{liga}_next.csv"
df.to_csv(filename, sep=";", index=False)