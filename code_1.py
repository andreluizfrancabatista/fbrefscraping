import sys
import os
import subprocess

paises = ['inglaterra', 'italia', 'espanha', 'alemanha', 'frança']

arquivo = "data/backtesting_resultados.csv"

# Verifica se o arquivo existe antes de deletar
if os.path.exists(arquivo):
    os.remove(arquivo)
    print(f"{arquivo} deletado com sucesso!")
else:
    print(f"{arquivo} não encontrado.")

for pais in paises:
    # Executa index.py
    # subprocess.run(["python", "index.py", pais], check=True)
    pass

for pais in paises:
    # Executa scores_semanais.py
    # subprocess.run(["python", "scores_semanais.py", pais], check=True)
    pass

for pais in paises:
    # Executa backtesting.py
    subprocess.run(["python", "backtesting.py", pais], check=True)
