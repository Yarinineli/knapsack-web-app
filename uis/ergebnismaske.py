import streamlit as st
import plotly.express as px
from navigate import navigate, clear_inputs
from algorithms import greedy_knapsack, dynamic_programming_knapsack, gurobi_knapsack

def ergebnismaske(pages):
    st.title("Ergebnismaske")
    st.write("Die Ergebnisse der ausgewählten Algorithmen werden präsentiert.")
    
    # Check if bag size is set
    if "bag_size" not in st.session_state:
        st.error("Keine Taschengröße ausgewählt. Bitte kehren Sie zur Taschenauswahl zurück.")
        return
    
    bag_size = st.session_state["bag_size"]
    weight_limit = st.session_state["weight_limits"][bag_size]
    
    # Check if items are selected
    if "gegenstände_df" not in st.session_state or st.session_state["gegenstände_df"].empty:
        st.error("Keine Gegenstände ausgewählt. Bitte fügen Sie Gegenstände hinzu.")
        return
    
    # Perform algorithm calculations
    greedy_selected_items, greedy_total_weight, greedy_total_value = greedy_knapsack(
        st.session_state["gegenstände_df"], 
        weight_limit,
        strategy='efficiency'
    )
    
    dp_selected_items, dp_total_weight, dp_total_value = dynamic_programming_knapsack(
        st.session_state["gegenstände_df"], 
        weight_limit
    )
    
    gurobi_selected_items, gurobi_total_weight, gurobi_total_value = gurobi_knapsack(
        st.session_state["gegenstände_df"], 
        weight_limit
    )
    
    # Metriken anzeigen
    st.header('Algorithmus-Metriken')
    col1, col2, col3 = st.columns(3)
    
    # Greedy Metrics
    col1.metric('Anzahl Gegenstände (Greedy)', len(greedy_selected_items))
    col2.metric('Gesamtgewicht (Greedy)', f'{greedy_total_weight:.2f} kg')
    col3.metric('Gesamtnutzen (Greedy)', f'{greedy_total_value:.0f} Punkte')
    
    # Dynamic Programming Metrics
    col1.metric('Anzahl Gegenstände (DP)', len(dp_selected_items))
    col2.metric('Gesamtgewicht (DP)', f'{dp_total_weight:.2f} kg')
    col3.metric('Gesamtnutzen (DP)', f'{dp_total_value:.0f} Punkte')
    
    # Gurobi Metrics
    col1.metric('Anzahl Gegenstände (Gurobi)', len(gurobi_selected_items))
    col2.metric('Gesamtgewicht (Gurobi)', f'{gurobi_total_weight:.2f} kg')
    col3.metric('Gesamtnutzen (Gurobi)', f'{gurobi_total_value:.0f} Punkte')
    
    # Selected Items Details
    st.header('Ausgewählte Gegenstände')
    
    # Gurobi Solver Results
    st.subheader('Gurobi Solver')
    if not gurobi_selected_items.empty:
        st.dataframe(
            gurobi_selected_items[['Gegenstand', 'Gewicht (kg)', 'Nutzen']]
            .sort_values('Nutzen', ascending=False)
            .style.format({
                'Gewicht (kg)': '{:.2f}',
                'Nutzen': '{:.0f}'
            })
        )
    
    # Greedy Algorithm Results
    st.subheader('Greedy Algorithmus')
    if not greedy_selected_items.empty:
        greedy_selected_items['Effizienz'] = greedy_selected_items['Nutzen'] / greedy_selected_items['Gewicht (kg)']
        st.dataframe(
            greedy_selected_items[['Gegenstand', 'Gewicht (kg)', 'Nutzen', 'Effizienz']]
            .sort_values('Nutzen', ascending=False)
            .style.format({
                'Gewicht (kg)': '{:.2f}',
                'Effizienz': '{:.2f}',
                'Nutzen': '{:.0f}'
            })
        )
    
    # Dynamic Programming Results
    st.subheader('Dynamische Programmierung')
    if not dp_selected_items.empty:
        st.dataframe(
            dp_selected_items[['Gegenstand', 'Gewicht (kg)', 'Nutzen']]
            .sort_values('Nutzen', ascending=False)
            .style.format({
                'Gewicht (kg)': '{:.2f}',
                'Nutzen': '{:.0f}'
            })
        )
    
    # Gewichtsverteilung
    st.header('Gewichtsverteilung')
    
    # Greedy Weight Distribution
    if not greedy_selected_items.empty:
        fig_greedy = px.pie(
            greedy_selected_items,
            values='Gewicht (kg)',
            names='Gegenstand',
            title='Gewichtsverteilung der ausgewählten Gegenstände (Greedy)',
            hole=0.3
        )
        fig_greedy.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_greedy)
    
    # Dynamic Programming Weight Distribution
    if not dp_selected_items.empty:
        fig_dp = px.pie(
            dp_selected_items,
            values='Gewicht (kg)',
            names='Gegenstand',
            title='Gewichtsverteilung der ausgewählten Gegenstände (DP)',
            hole=0.3
        )
        fig_dp.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_dp)
    
    # Nutzenverteilung
    st.header('Nutzenverteilung')
    
    # Greedy Value Distribution
    if not greedy_selected_items.empty:
        fig_value_greedy = px.pie(
            greedy_selected_items,
            values='Nutzen',
            names='Gegenstand',
            title='Nutzenverteilung der ausgewählten Gegenstände (Greedy)',
            hole=0.3
        )
        fig_value_greedy.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_value_greedy)
    
    # Dynamic Programming Value Distribution
    if not dp_selected_items.empty:
        fig_value_dp = px.pie(
            dp_selected_items,
            values='Nutzen',
            names='Gegenstand',
            title='Nutzenverteilung der ausgewählten Gegenstände (DP)',
            hole=0.3
        )
        fig_value_dp.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_value_dp)
    
    # Back to start button
    if st.button("Zurück zur Startseite"):
        clear_inputs()
        navigate("Start")