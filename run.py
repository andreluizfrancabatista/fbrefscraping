import sys
import subprocess

if len(sys.argv) > 1:
    pais = sys.argv[1]

    # Executa index.py
    subprocess.run(["python", "index.py", pais], check=True)

    # Executa chance.py
    subprocess.run(["python", "chance.py", pais], check=True)
else:
    print("Erro: Nenhum país foi fornecido.")
    sys.exit(1)
