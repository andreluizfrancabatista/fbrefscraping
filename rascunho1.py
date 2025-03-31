# Escolha da campeonato
liga = {
    "colombia" : "https://fbref.com/en/comps/41/schedule/Primera-A-Scores-and-Fixtures"
}

pais = "colombia"

print(f'{pais} - {liga.get(pais)}')