import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from data.data import df
from gurobipy import Model, GRB, quicksum
from uis.start_page import start_page
from uis.eingabemaske_tasche import eingabemaske_tasche
from uis.uebersichtsmaske import uebersichtsmaske
from uis.algorithmen_auswahlmaske import algorithmen_auswahlmaske
from uis.ladescreen import ladescreen
from uis.ergebnismaske import ergebnismaske
from uis.eingabemaske_gegenstände import eingabemaske_gegenstände
from navigate import navigate


def dynamic_programming_knapsack(items_df, weight_limit):
    """
    Implementiert den Knapsack-Algorithmus mit dynamischer Programmierung
    """
    
    if items_df.empty:
        return pd.DataFrame(), 0, 0  # Rückgabe eines leeren DataFrames und Nullwerten
    
    n = len(items_df)
    weights = items_df['Gewicht'].values
    values = items_df['Nutzen'].values
    
    # Gewichte in Integer umwandeln für die DP-Matrix (multipliziere mit 10 für eine Dezimalstelle)
    weight_multiplier = 10
    weights = (weights * weight_multiplier).astype(int)
    weight_limit_scaled = int(weight_limit * weight_multiplier)
    
    # DP-Matrix erstellen
    dp = np.zeros((n + 1, weight_limit_scaled + 1))
    keep = np.zeros((n + 1, weight_limit_scaled + 1), dtype=bool)
    
    # DP-Matrix füllen
    for i in range(1, n + 1):
        for w in range(weight_limit_scaled + 1):
            
            if weights[i-1] <= w: #Fall 1: Der Gegenstand passt in den Rucksack
                
                without_item = dp[i-1][w]
                with_item = dp[i-1][w-weights[i-1]] + values[i-1]
                if with_item > without_item:
                    dp[i][w] = with_item
                    keep[i][w] = True
                else:
                    dp[i][w] = without_item
            
            else:                #Fall 2: Der Gegenstand passt nicht in den Rucksack
                dp[i][w] = dp[i-1][w]
    
    # Ausgewählte Items zurückverfolgen
    selected_items = []
    w = weight_limit_scaled
    total_weight = 0
    for i in range(n, 0, -1):
        if keep[i][w] and total_weight + items_df.iloc[i-1]['Gewicht'] <= weight_limit:
            selected_items.append(items_df.iloc[i-1])
            total_weight += items_df.iloc[i-1]['Gewicht']
            w -= weights[i-1]
            
    if not selected_items:  # Keine Items ausgewählt
        return pd.DataFrame(), 0, 0
    
    selected_df = pd.DataFrame(selected_items)
    total_weight = selected_df['Gewicht'].sum()
    total_value = selected_df['Nutzen'].sum()
    
    return selected_df, total_weight, total_value

def greedy_knapsack(items_df, weight_limit, strategy='efficiency'):
    """
    Implementiert den Greedy-Algorithmus für das Knapsack Problem
    """
    if items_df.empty:
        return pd.DataFrame(), 0, 0
    
    df_copy = items_df.copy()
    df_copy['Effizienz'] = df_copy['Nutzen'] / df_copy['Gewicht']
    
    if strategy == 'efficiency':
        df_copy = df_copy.sort_values('Effizienz', ascending=False)
    elif strategy == 'value':
        df_copy = df_copy.sort_values('Nutzen', ascending=False)
    elif strategy == 'weight':
        df_copy = df_copy.sort_values('Gewicht')
    
    selected_items = []
    total_weight = 0
    total_value = 0
    
    for _, item in df_copy.iterrows():
        if total_weight + item['Gewicht'] <= weight_limit:
            selected_items.append(item)
            total_weight += item['Gewicht']
            total_value += item['Nutzen']
    
    if not selected_items:  # Keine Items ausgewählt
        return pd.DataFrame(), 0, 0
    
    return pd.DataFrame(selected_items), total_weight, total_value

def gurobi_knapsack(items_df, weight_limit):
    """
    Löst das Knapsack-Problem mit dem Gurobi Solver.
    """
    # Gurobi-Modell erstellen
    model = Model("Knapsack Problem")
    model.setParam("OutputFlag", 0)  # Keine Ausgabe in der Konsole

    # Variablen erstellen (0 oder 1 für jeden Gegenstand)
    items = items_df.index
    item_included = model.addVars(items, vtype=GRB.BINARY, name="item_included")

    # Ziel: Gesamtnutzen maximieren
    model.setObjective(quicksum(items_df.loc[i, 'Nutzen'] * item_included[i] for i in items), GRB.MAXIMIZE)

    # Einschränkung: Gewichtslimit einhalten
    model.addConstr(quicksum(items_df.loc[i, 'Gewicht'] * item_included[i] for i in items) <= weight_limit, "Gewichtslimit")

    # Optimierung starten
    model.optimize()

    # Ergebnisse abrufen
    selected_items = []
    total_weight = 0
    total_value = 0

    if model.status == GRB.OPTIMAL:
        for i in items:
            if item_included[i].X > 0.5:  # Wenn Gegenstand ausgewählt wurde
                selected_items.append(items_df.loc[i])
                total_weight += items_df.loc[i, 'Gewicht']
                total_value += items_df.loc[i, 'Nutzen']

    selected_df = pd.DataFrame(selected_items)
    return selected_df, total_weight, total_value


# Seiten-Definitionen
st.logo("./images/HSBI_Logo_RGB_schwarz.png", size="large")
st.set_page_config(
    page_title="Knapsack Problem",
    page_icon="🎒",
    layout="wide",
)

pages = {
    "Start": lambda: start_page(pages),
    "Eingabemaske_Tasche": lambda: eingabemaske_tasche(pages),
    "Eingabemaske_Gegenstände": lambda: eingabemaske_gegenstände(pages),
    "Algorithmen-Auswahlmaske": lambda: algorithmen_auswahlmaske(pages),
    "Übersichtsmaske": lambda: uebersichtsmaske(pages),
    "Ladescreen": lambda: ladescreen(pages),
    "Ergebnismaske": lambda: ergebnismaske(pages),
}

# Startpunkt der Anwendung
if "page" not in st.session_state:
    st.session_state.page = "Start"
pages[st.session_state.page]()