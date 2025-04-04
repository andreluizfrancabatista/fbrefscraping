import pandas as pd
import sys
import os

pd.set_option("display.precision", 2)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_columns', None)
pd.options.display.float_format = '{:.2f}'.format

if len(sys.argv) > 1:
    pais = sys.argv[1]
    liga = sys.argv[2]
    link = sys.argv[3]

# Carregar os CSVs
df_matches = pd.read_csv(f'data/{pais}-{liga}.csv', sep=';')
df_scores = pd.read_csv(f'data/{pais}-{liga}_scores.csv', sep=';', index_col=0)

# Garantir que as colunas de week no df_scores sejam strings no formato correto (ex: 'WEEK2', 'WEEK3'...)
df_scores.columns = [f'WEEK{int(col.replace("WEEK", ""))}' for col in df_scores.columns]

# Criar colunas para armazenar os scores
df_matches['HOME_SCORE'] = 0.0
df_matches['AWAY_SCORE'] = 0.0

# Preencher os scores corretamente
for i, row in df_matches.iterrows():
    week = f'WEEK{row["WEEK"]}'
    
    if week in df_scores.columns:
        home_team = row["HOME"]
        away_team = row["AWAY"]

        if home_team in df_scores.index:
            df_matches.at[i, 'HOME_SCORE'] = df_scores.at[home_team, week]
        
        if away_team in df_scores.index:
            df_matches.at[i, 'AWAY_SCORE'] = df_scores.at[away_team, week]

# Criar a coluna DIFF_SCORE
df_matches['DIFF_SCORE'] = df_matches['HOME_SCORE'] - df_matches['AWAY_SCORE']

# Criar a coluna FTR_DIFF
df_matches['DIFF_FTR'] = df_matches.apply(lambda row: 'H' if row['DIFF_SCORE'] >= 1.5 else ('A' if row['DIFF_SCORE'] <= -1.5 else 'D'), axis=1)

# Criar a coluna FTR
df_matches['FTR'] = df_matches.apply(lambda row: 'H' if row['FTHG'] > row['FTAG'] else ('A' if row['FTAG'] > row['FTHG'] else 'D'), axis=1)

# Criar a coluna country
df_matches['COUNTRY'] = pais

# Criar a coluna league
df_matches['LEAGUE'] = liga

# Reorganizar colunas
colunas = ['COUNTRY', 'LEAGUE', 'WEEK', 'DATE', 'HOME', 'AWAY', 'FTHG', 'FTAG', 'FTR', 'HOME_SCORE', 'AWAY_SCORE', 'DIFF_SCORE', 'DIFF_FTR']
df_matches = df_matches[colunas]

# Salvar o resultado final
df_matches.to_csv(f'data/{pais}-{liga}_final.csv', sep=';', index=False)
# print(df_matches.tail(10))


#####
# Contar os acertos
#####
# # Gerar relatório
# Cálculo dos totais
total_jogos = len(df_matches)
total_diff_ftr_h = len(df_matches[df_matches['DIFF_FTR'] == 'H'])
total_diff_ftr_a = len(df_matches[df_matches['DIFF_FTR'] == 'A'])
total_diff_ftr_h_ftr_hd = len(df_matches[(df_matches['DIFF_FTR'] == 'H') & (df_matches['FTR'].isin(['H', 'D']))])
total_diff_ftr_a_ftr_ad = len(df_matches[(df_matches['DIFF_FTR'] == 'A') & (df_matches['FTR'].isin(['A', 'D']))])

# Evitar divisão por zero
porcentagem_acertos_h = (total_diff_ftr_h_ftr_hd / total_diff_ftr_h) if total_diff_ftr_h > 0 else 0
porcentagem_acertos_a = (total_diff_ftr_a_ftr_ad / total_diff_ftr_a) if total_diff_ftr_a > 0 else 0
porcentagem_acertos_total = ((total_diff_ftr_h_ftr_hd + total_diff_ftr_a_ftr_ad) / (total_diff_ftr_h + total_diff_ftr_a)) if (total_diff_ftr_h + total_diff_ftr_a) > 0 else 0

#Capitalizar país
pais = pais.capitalize()

# Criar DataFrame com os resultados
df_resultado = pd.DataFrame([[  
    pais, liga, total_jogos, total_diff_ftr_h, total_diff_ftr_a,  
    total_diff_ftr_h_ftr_hd, total_diff_ftr_a_ftr_ad,  
    round(porcentagem_acertos_h, 2), round(porcentagem_acertos_a, 2), round(porcentagem_acertos_total, 2)  
]], columns=[  
    'COUNTRY', 'LEAGUE', 'Total Jogos', 'DIFF_FTR = H', 'DIFF_FTR = A',  
    'DIFF_FTR = H e FTR = H ou D', 'DIFF_FTR = A e FTR = A ou D',  
    '% acertos H', '% acertos A', '% acertos total'  
])

# Caminho do CSV consolidado
output_file = "data/backtesting_resultados.csv"

# Verifica se o arquivo já existe e salva os dados
if os.path.exists(output_file):
    df_resultado.to_csv(output_file, sep=';', mode='a', header=False, index=False, decimal=',')  # Anexa sem cabeçalho
else:
    df_resultado.to_csv(output_file, sep=';', index=False, decimal=',')  # Cria o arquivo com cabeçalho

# print(f"Dados de {pais} adicionados ao CSV consolidado.")
print(f'{pais:<13} {liga:<17} H: {round(porcentagem_acertos_h*100, 2):<5}%. A: {round(porcentagem_acertos_a*100, 2):<5}%. Total: {round(porcentagem_acertos_total*100, 2):<5}%')