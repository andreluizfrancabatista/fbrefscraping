import sys
import pandas as pd
import numpy as np
from collections import defaultdict

pd.set_option("display.precision", 2)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_columns', None)
pd.options.display.float_format = '{:.2f}'.format

def build_system_from_df(df, teams):
    home_teams = df['HOME'].values
    away_teams = df['AWAY'].values
    diffs = df['DIFF'].values
    var_index = {var: idx for idx, var in enumerate(teams)}
    A = np.zeros((len(df), len(teams)))
    b = np.zeros(len(df))
    for i in range(len(df)):
        A[i, var_index[home_teams[i]]] = 1
        A[i, var_index[away_teams[i]]] = -1
        b[i] = diffs[i]
    return A, b, teams

def solve_system_for_week(df, teams):
    A, b, variables = build_system_from_df(df, teams)
    x, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
    return {variables[i]: x[i] for i in range(len(variables))}

def compute_weekly_scores(file_path):
    df = pd.read_csv(file_path, sep=';')
    df['WEEK'] = df['WEEK'].astype(int)  # Garante que WEEK seja int
    weeks = sorted(df['WEEK'].unique())
    weeks.append(weeks[-1] + 1) # Adiciona a próxima semana
    teams = sorted(set(df['HOME']).union(set(df['AWAY'])))
    results = defaultdict(lambda: defaultdict(float))  # Default para evitar NaN
    for week in weeks[1:]:  # Começando da segunda semana
        df_week = df[df['WEEK'] < week]
        scores = solve_system_for_week(df_week, teams)
        for team in teams:
            results[team][f'WEEK{week}'] = scores.get(team, 0)
    return pd.DataFrame.from_dict(results, orient='index')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        pais = sys.argv[1]
        liga = sys.argv[2]
        link = sys.argv[3]
    file_path = f'data/{pais}-{liga}.csv'
    df_weekly_scores = compute_weekly_scores(file_path)
    df_weekly_scores.to_csv(f'data/{pais}-{liga}_scores.csv', sep=';', index=True)

