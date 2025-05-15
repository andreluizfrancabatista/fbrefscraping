# Para gerar o arquivo csv com todos os next matches
import os
import subprocess

arquivo = "data/all_next.csv"

# Verifica se o arquivo existe antes de deletar
if os.path.exists(arquivo):
    print(f'{arquivo} encontrado!')
    os.remove(arquivo)
    print(f"{arquivo} deletado com sucesso!")
else:
    print(f"{arquivo} não encontrado.")

dataset = {
    "inglaterra" : {
        "E0" : "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures",
        "E1" : "https://fbref.com/en/comps/10/schedule/Championship-Scores-and-Fixtures",
        "E2" : "https://fbref.com/en/comps/15/schedule/League-One-Scores-and-Fixtures",
        "E3" : "https://fbref.com/en/comps/16/schedule/League-Two-Scores-and-Fixtures",
        "EC" : "https://fbref.com/en/comps/34/schedule/National-League-Scores-and-Fixtures"
    },
    "espanha" : {
        "SP1" : "https://fbref.com/en/comps/12/schedule/La-Liga-Scores-and-Fixtures",
        "SP2" : "https://fbref.com/en/comps/17/schedule/Segunda-Division-Scores-and-Fixtures"
    },
    "italia" : {
        "I1" : "https://fbref.com/en/comps/11/schedule/Serie-A-Scores-and-Fixtures",
        "I2" : "https://fbref.com/en/comps/18/schedule/Serie-B-Scores-and-Fixtures"
    },
    "alemanha" : {
        "D1" : "https://fbref.com/en/comps/20/schedule/Bundesliga-Scores-and-Fixtures",
        "D2" : "https://fbref.com/en/comps/33/schedule/2-Bundesliga-Scores-and-Fixtures"
    },
    "frança" : {
        "F1" : "https://fbref.com/en/comps/13/schedule/Ligue-1-Scores-and-Fixtures",
        "F2" : "https://fbref.com/en/comps/60/schedule/Ligue-2-Scores-and-Fixtures"
    },
    "bélgica" : {
      "B1" : "https://fbref.com/en/comps/37/schedule/Belgian-Pro-League-Scores-and-Fixtures"
   },
   "grécia" : {
      "G1" : "https://fbref.com/en/comps/27/schedule/Super-League-Greece-Scores-and-Fixtures"
   },
   "portugal" : {
      "P1" : "https://fbref.com/en/comps/32/schedule/Primeira-Liga-Scores-and-Fixtures"
   },
   "escócia" : {
      "SC0" : "https://fbref.com/en/comps/40/schedule/Scottish-Premiership-Scores-and-Fixtures",
      "SC1" : "https://fbref.com/en/comps/72/schedule/Scottish-Championship-Scores-and-Fixtures"
   },
   "turquia" : {
      "T1" : "https://fbref.com/en/comps/26/schedule/Super-Lig-Scores-and-Fixtures"
   }
}

scripts = ["gera_next.py"]

for script in scripts:
  for pais, obj in dataset.items():
    for liga, link in obj.items():
      subprocess.run(["python", script, pais, liga, link], check=True)
