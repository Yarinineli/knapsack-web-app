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
    
    # Display results in three columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Greedy Algorithmus")
        st.metric('Anzahl Gegenstände', len(greedy_selected_items))
        st.metric('Gesamtgewicht', f'{greedy_total_weight:.2f} kg')
        st.metric('Gesamtnutzen', f'{greedy_total_value:.0f} Punkte')
        
        if not greedy_selected_items.empty:
            st.dataframe(
                greedy_selected_items[['Gegenstand', 'Gewicht (kg)', 'Nutzen']]
                .sort_values('Nutzen', ascending=False)
            )
            fig_greedy = px.pie(
                greedy_selected_items,
                values='Gewicht (kg)',
                names='Gegenstand',
                title='Gewichtsverteilung (Greedy)',
                hole=0.3
            )
            st.plotly_chart(fig_greedy, use_container_width=True)
    
    with col2:
        st.subheader("Dynamische Programmierung")
        st.metric('Anzahl Gegenstände', len(dp_selected_items))
        st.metric('Gesamtgewicht', f'{dp_total_weight:.2f} kg')
        st.metric('Gesamtnutzen', f'{dp_total_value:.0f} Punkte')
        
        if not dp_selected_items.empty:
            st.dataframe(
                dp_selected_items[['Gegenstand', 'Gewicht (kg)', 'Nutzen']]
                .sort_values('Nutzen', ascending=False)
            )
            fig_dp = px.pie(
                dp_selected_items,
                values='Gewicht (kg)',
                names='Gegenstand',
                title='Gewichtsverteilung (DP)',
                hole=0.3
            )
            st.plotly_chart(fig_dp, use_container_width=True)
    
    with col3:
        st.subheader("Gurobi Solver")
        st.metric('Anzahl Gegenstände', len(gurobi_selected_items))
        st.metric('Gesamtgewicht', f'{gurobi_total_weight:.2f} kg')
        st.metric('Gesamtnutzen', f'{gurobi_total_value:.0f} Punkte')
        
        if not gurobi_selected_items.empty:
            st.dataframe(
                gurobi_selected_items[['Gegenstand', 'Gewicht (kg)', 'Nutzen']]
                .sort_values('Nutzen', ascending=False)
            )
            fig_gurobi = px.pie(
                gurobi_selected_items,
                values='Gewicht (kg)',
                names='Gegenstand',
                title='Gewichtsverteilung (Gurobi)',
                hole=0.3
            )
            st.plotly_chart(fig_gurobi, use_container_width=True)

    # Back to start button
    if st.button("Zurück zur Startseite"):
        clear_inputs()
        navigate("Start", pages)
