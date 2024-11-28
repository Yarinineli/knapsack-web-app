import streamlit as st
from navigate import navigate, clear_inputs
from algorithms import greedy_knapsack, dynamic_programming_knapsack, gurobi_knapsack

def ergebnismaske(pages):
    st.title("Ergebnismaske")
    st.write("Die Ergebnisse der ausgewählten Algorithmen werden präsentiert.")
    
    if st.session_state["greedy"] == True:
        st.subheader("Greedy-Algorithmus")
        st.write("Hier werden die Ergebnisse des Greedy-Algorithmus präsentiert.")
        greedy_results = greedy_knapsack(st.session_state["gegenstände_df"], st.session_state["bag_size"])
        st.write(greedy_results)
        
    
    
    
    if st.button("Zurück zur Startseite"):
        clear_inputs()
        navigate("Start")