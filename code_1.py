import sys
import os
import subprocess

paises = ['inglaterra-1', 'inglaterra-2', 'italia-1', 'italia-2', 'espanha-1', 'espanha-2', 'alemanha-1', 'alemanha-2', 'frança-1', 'frança-2']

arquivo = "data/backtesting_resultados.csv"

# Verifica se o arquivo existe antes de deletar
if os.path.exists(arquivo):
    os.remove(arquivo)
    print(f"{arquivo} deletado com sucesso!")
else:
    print(f"{arquivo} não encontrado.")

for pais in paises:
    # Executa index.py
    subprocess.run(["python", "index.py", pais], check=True)
    # pass

for pais in paises:
    # Executa scores_semanais.py
    subprocess.run(["python", "scores_semanais.py", pais], check=True)
    # pass

for pais in paises:
    # Executa backtesting.py
    subprocess.run(["python", "backtesting.py", pais], check=True)
