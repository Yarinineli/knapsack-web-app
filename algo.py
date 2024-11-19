import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from data.data import df

def dynamic_programming_knapsack(items_df, weight_limit):
    """
    Implementiert den Knapsack-Algorithmus mit dynamischer Programmierung
    """
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
    
    selected_df = pd.DataFrame(selected_items)
    total_weight = selected_df['Gewicht'].sum()
    total_value = selected_df['Nutzen'].sum()
    
    return selected_df, total_weight, total_value

def greedy_knapsack(items_df, weight_limit, strategy='efficiency'):
    """
    Implementiert den Greedy-Algorithmus für das Knapsack Problem
    """
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
    
    for idx, item in df_copy.iterrows():
        if total_weight + item['Gewicht'] <= weight_limit:
            selected_items.append(item)
            total_weight += item['Gewicht']
            total_value += item['Nutzen']
    
    return pd.DataFrame(selected_items), total_weight, total_value


# Streamlit Interface
st.logo("./images/HSBI_Logo_RGB_schwarz.png", size="large")
st.title('Knapsack Problem')

# Import required library
from streamlit_image_select import image_select

# Auswahl der Taschengröße with images
st.header('1. Wähle deine Taschengröße')

# Image selection for bag sizes
bag_image = image_select(
    label="Wähle eine Taschengröße",
    images=[
        "./images/HSBI_Logo_RGB_schwarz.png",  # Local image file for 'Klein'
        "./images/HSBI_Logo_RGB_schwarz.png",  # Local image file for 'Mittel'
        "./images/HSBI_Logo_RGB_schwarz.png",  # Local image file for 'Groß'
    ],
    captions=["Klein (5 kg)", "Mittel (10 kg)", "Groß (15 kg)"],  # Descriptive captions
    use_container_width=True
)

# Map selected image to corresponding bag size
if bag_image == "./images/HSBI_Logo_RGB_schwarz.png":
    bag_size = "Klein (5 kg)"
elif bag_image == "./images/HSBI_Logo_RGB_schwarz.png":
    bag_size = "Mittel (10 kg)"
elif bag_image == "./images/HSBI_Logo_RGB_schwarz.png":
    bag_size = "Groß (15 kg)"

# Display selected bag size
st.write(f"Ausgewählte Taschengröße: {bag_size}")

# Mapping bag sizes to their weight limits
weight_limits = {
    "Klein (5 kg)": 5.0,
    "Mittel (10 kg)": 10.0,
    "Groß (15 kg)": 15.0
}


# # Auswahl der Taschengröße
# st.header('1. Wähle deine Taschengröße')
# bag_size = st.radio(
#     'Verfügbare Taschen:',
#     ['Klein (5 kg)', 'Mittel (10 kg)', 'Groß (15 kg)']
# )
# # Klickbare Bilder für die Taschengröße
# st.header('1. Wähle deine Taschengröße')
# col1, col2, col3 = st.columns(3)

# with col1:
#     if st.button('Klein (5 kg)'):
#         bag_size = 'Klein (5 kg)'
#     st.image('./images/HSBI_Logo_RGB_schwarz.png', caption='Klein (5 kg)', use_container_width=True)

# with col2:
#     if st.button('Mittel (10 kg)'):
#         bag_size = 'Mittel (10 kg)'
#     st.image('./images/HSBI_Logo_RGB_schwarz.png', caption='Mittel (10 kg)', use_container_width=True)

# with col3:
#     if st.button('Groß (15 kg)'):
#         bag_size = 'Groß (15 kg)'
#     st.image('./images/HSBI_Logo_RGB_schwarz.png', caption='Groß (15 kg)', use_container_width=True)

# Mapping der Taschengrößen zu Gewichtslimits
# weight_limits = {
#     'Klein (5 kg)': 5.0,
#     'Mittel (10 kg)': 10.0,
#     'Groß (15 kg)': 15.0
# }

# Strategie für Greedy Algorithmus
st.header('2. Wähle deine Packstrategie für den Greedy Algorithmus')
strategy = st.selectbox(
    'Strategie:',
    ['Effizienz (Nutzen/Gewicht)', 'Maximaler Nutzen', 'Minimales Gewicht'],
    help="""Effizienz bevorzugt  Gegenstände mit bestem  Nutzen-Gewicht-Verhältnis"""
)

# Mapping der Strategien
strategy_mapping = {
    'Effizienz (Nutzen/Gewicht)': 'efficiency',
    'Maximaler Nutzen': 'value',
    'Minimales Gewicht': 'weight'
}

if st.button('Packliste erstellen'):
    # Greedy Algorithmus ausführen
    greedy_selected_items, greedy_total_weight, greedy_total_value = greedy_knapsack(
        df, 
        weight_limits[bag_size],
        strategy_mapping[strategy]
    )
    
    # Dynamische Programmierung ausführen
    dp_selected_items, dp_total_weight, dp_total_value = dynamic_programming_knapsack(
        df,
        weight_limits[bag_size]
    )
    
    # Ergebnisse anzeigen
    st.header('Deine optimierte Packliste:')
    
    # Metriken anzeigen
    col1, col2, col3 = st.columns(3)
    col1.metric('Anzahl Gegenstände (Greedy)', len(greedy_selected_items))
    col2.metric('Gesamtgewicht (Greedy)', f'{greedy_total_weight:.2f} kg')
    col3.metric('Gesamtnutzen (Greedy)', f'{greedy_total_value:.0f} Punkte')
    
    col1.metric('Anzahl Gegenstände (DP)', len(dp_selected_items))
    col2.metric('Gesamtgewicht (DP)', f'{dp_total_weight:.2f} kg')
    col3.metric('Gesamtnutzen (DP)', f'{dp_total_value:.0f} Punkte')
    
    # Ausgewählte Gegenstände anzeigen
    st.subheader('Greedy Algorithmus')
    greedy_selected_items['Effizienz'] = greedy_selected_items['Nutzen'] / greedy_selected_items['Gewicht']
    st.dataframe(
        greedy_selected_items[['Gegenstand', 'Gewicht', 'Nutzen', 'Effizienz']]
        .sort_values('Nutzen', ascending=False)
        .style.format({
            'Gewicht': '{:.2f}',
            'Effizienz': '{:.2f}',
            'Nutzen': '{:.0f}'
        })
    )
    
    st.subheader('Dynamische Programmierung')
    st.dataframe(
        dp_selected_items[['Gegenstand', 'Gewicht', 'Nutzen']]
        .sort_values('Nutzen', ascending=False)
        .style.format({
            'Gewicht': '{:.2f}',
            'Nutzen': '{:.0f}'
        })
    )
    
    # Visualisierung mit Pie Chart
    st.header('Gewichtsverteilung')
    
    # Pie Chart mit Plotly Express für Greedy Algorithmus
    fig_greedy = px.pie(
        greedy_selected_items,
        values='Gewicht',
        names='Gegenstand',
        title='Gewichtsverteilung der ausgewählten Gegenstände (Greedy)',
        hole=0.3
    )
    fig_greedy.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_greedy)

    # Pie Chart mit Plotly Express für Dynamische Programmierung
    fig_dp = px.pie(
        dp_selected_items,
        values='Gewicht',
        names='Gegenstand',
        title='Gewichtsverteilung der ausgewählten Gegenstände (DP)',
        hole=0.3
    )
    fig_dp.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_dp)

    # Nutzenverteilung
    st.header('Nutzenverteilung')
    
    # Pie Chart mit Plotly Express für Greedy Algorithmus
    fig_value_greedy = px.pie(
        greedy_selected_items,
        values='Nutzen',
        names='Gegenstand',
        title='Nutzenverteilung der ausgewählten Gegenstände (Greedy)',
        hole=0.3
    )
    fig_value_greedy.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_value_greedy)

    # Pie Chart mit Plotly Express für Dynamische Programmierung
    fig_value_dp = px.pie(
        dp_selected_items,
        values='Nutzen',
        names='Gegenstand',
        title='Nutzenverteilung der ausgewählten Gegenstände (DP)',
        hole=0.3
    )
    fig_value_dp.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_value_dp)

# Ursprüngliche Datenbank anzeigen
st.header('Verfügbare Gegenstände')
st.dataframe(df)