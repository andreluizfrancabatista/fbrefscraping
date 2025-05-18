import os
import subprocess

dataset = {
    "brasil" : {
        "Série A" : "https://fbref.com/en/comps/24/schedule/Serie-A-Scores-and-Fixtures",
        "Série B" : "https://fbref.com/en/comps/38/schedule/Serie-B-Scores-and-Fixtures"
    },
    "bolivia" : {
       "Primera Div" : "https://fbref.com/en/comps/74/schedule/Bolivian-Primera-Division-Scores-and-Fixtures"
    },
    "chile" : {
        "Primera Div" : "https://fbref.com/en/comps/35/schedule/Chilean-Primera-Division-Scores-and-Fixtures"
    },
    # "colombia" : {
    #     "Primera A" : "https://fbref.com/en/comps/41/schedule/Primera-A-Scores-and-Fixtures"
    # },
    "ecuador" : {
        "Serie A" : "https://fbref.com/en/comps/58/schedule/Serie-A-Scores-and-Fixtures"
    },
    "peru" : {
       "Liga 1" : "https://fbref.com/en/comps/44/schedule/Liga-1-Scores-and-Fixtures"
    },
    "uruguay" : {
        "Primera Div" : "https://fbref.com/en/comps/45/schedule/Uruguayan-Primera-Division-Scores-and-Fixtures"
    }
    # "venezuela" : {
    #    "Primera Div" : "https://fbref.com/en/comps/105/schedule/Venezuelan-Primera-Division-Scores-and-Fixtures"
    # }
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
