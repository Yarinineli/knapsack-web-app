import numpy as np
import pandas as pd
from gurobipy import Model, GRB, quicksum
import time

def algorithm_metrics(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        return (*result, execution_time)
    return wrapper

@algorithm_metrics
def dynamic_programming_knapsack(items_df, weight_limit):
    """
    Implementiert den Knapsack-Algorithmus mit dynamischer Programmierung
    """
    if items_df.empty:
        return pd.DataFrame(), 0, 0

    n = len(items_df)
    weights = items_df['Gewicht (kg)'].values
    values = items_df['Nutzen'].values
    
    weight_multiplier = 10
    weights = (weights * weight_multiplier).astype(int)
    weight_limit_scaled = int(weight_limit * weight_multiplier)
    
    dp = np.zeros((n + 1, weight_limit_scaled + 1))
    keep = np.zeros((n + 1, weight_limit_scaled + 1), dtype=bool)
    
    for i in range(1, n + 1):
        for w in range(weight_limit_scaled + 1):
            if weights[i-1] <= w:
                without_item = dp[i-1][w]
                with_item = dp[i-1][w-weights[i-1]] + values[i-1]
                if with_item > without_item:
                    dp[i][w] = with_item
                    keep[i][w] = True
                else:
                    dp[i][w] = without_item
            else:
                dp[i][w] = dp[i-1][w]
    
    selected_items = []
    total_weight = 0
    w = weight_limit_scaled
    for i in range(n, 0, -1):
        if keep[i][w] and total_weight + items_df.iloc[i-1]['Gewicht (kg)'] <= weight_limit:
            selected_items.append(items_df.iloc[i-1])
            total_weight += items_df.iloc[i-1]['Gewicht (kg)']
            w -= weights[i-1]
            
    if not selected_items:
        return pd.DataFrame(), 0, 0
    
    selected_df = pd.DataFrame(selected_items)
    total_value = selected_df['Nutzen'].sum()
    
    return selected_df, total_weight, total_value

@algorithm_metrics
def greedy_knapsack(items_df, weight_limit, strategy='efficiency'):
    """
    Implementiert den Greedy-Algorithmus für das Knapsack Problem
    """
    if items_df.empty:
        return pd.DataFrame(), 0, 0
    
    df_copy = items_df.copy()
    df_copy['Gewicht (kg)'] = pd.to_numeric(df_copy['Gewicht (kg)'], errors='coerce')
    df_copy['Effizienz'] = df_copy['Nutzen'] / df_copy['Gewicht (kg)']
    
    if strategy == 'efficiency':
        df_copy = df_copy.sort_values('Effizienz', ascending=False)
    elif strategy == 'value':
        df_copy = df_copy.sort_values('Nutzen', ascending=False)
    elif strategy == 'weight':
        df_copy = df_copy.sort_values('Gewicht (kg)')
    
    selected_items = []
    total_weight = 0
    total_value = 0
    
    for _, item in df_copy.iterrows():
        if total_weight + item['Gewicht (kg)'] <= weight_limit:
            selected_items.append(item)
            total_weight += item['Gewicht (kg)']
            total_value += item['Nutzen']
    
    if not selected_items:
        return pd.DataFrame(), 0, 0
    
    return pd.DataFrame(selected_items), total_weight, total_value

@algorithm_metrics
def gurobi_knapsack(items_df, weight_limit):
    """
    Löst das Knapsack-Problem mit dem Gurobi Solver.
    """
    model = Model("Knapsack Problem")
    model.setParam("OutputFlag", 0)

    items = items_df.index
    item_included = model.addVars(items, vtype=GRB.BINARY, name="item_included")

    model.setObjective(quicksum(items_df.loc[i, 'Nutzen'] * item_included[i] for i in items), GRB.MAXIMIZE)
    model.addConstr(quicksum(items_df.loc[i, 'Gewicht (kg)'] * item_included[i] for i in items) <= weight_limit, "Gewichtslimit")

    model.optimize()

    selected_items = []
    total_weight = 0
    total_value = 0

    if model.status == GRB.OPTIMAL:
        for i in items:
            if item_included[i].X > 0.5:
                selected_items.append(items_df.loc[i])
                total_weight += items_df.loc[i, 'Gewicht (kg)']
                total_value += items_df.loc[i, 'Nutzen']

    selected_df = pd.DataFrame(selected_items)
    return selected_df, total_weight, total_value