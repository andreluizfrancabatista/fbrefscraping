import sys
import os
import subprocess

dataset = {
    "inglaterra" : {
        "Premier League" : "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures",
        "EFL Championship" : "https://fbref.com/en/comps/10/schedule/Championship-Scores-and-Fixtures"
    },
    "espanha" : {
        "La Liga" : "https://fbref.com/en/comps/12/schedule/La-Liga-Scores-and-Fixtures",
        "La Liga 2" : "https://fbref.com/en/comps/17/schedule/Segunda-Division-Scores-and-Fixtures"
    },
    "italia" : {
        "Serie A" : "https://fbref.com/en/comps/11/schedule/Serie-A-Scores-and-Fixtures",
        "Serie B" : "https://fbref.com/en/comps/18/schedule/Serie-B-Scores-and-Fixtures"
    },
    "alemanha" : {
        "Bundesliga" : "https://fbref.com/en/comps/20/schedule/Bundesliga-Scores-and-Fixtures",
        "2. Bundesliga" : "https://fbref.com/en/comps/33/schedule/2-Bundesliga-Scores-and-Fixtures"
    },
    "frança" : {
        "Ligue 1" : "https://fbref.com/en/comps/13/schedule/Ligue-1-Scores-and-Fixtures",
        "Ligue 2" : "https://fbref.com/en/comps/60/schedule/Ligue-2-Scores-and-Fixtures"
    }
}

scripts = ["index.py", "scores_semanais.py", "backtesting.py"]
scripts = ["scores_semanais.py", "backtesting.py"]

for script in scripts:
  for pais, obj in dataset.items():
    for liga, link in obj.items():
      subprocess.run(["python", script, pais, liga, link], check=True)


arquivo = "data/backtesting_resultados.csv"

# Verifica se o arquivo existe antes de deletar
if os.path.exists(arquivo):
    os.remove(arquivo)
    print(f"{arquivo} deletado com sucesso!")
else:
    print(f"{arquivo} não encontrado.")
