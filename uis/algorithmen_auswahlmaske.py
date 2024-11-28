import streamlit as st
from navigate import navigate
import pandas as pd
from streamlit_extras import row
import numpy as np

def algorithmen_auswahlmaske(pages):

    tasche, gegenstände = st.columns([0.2, 0.8])
    with tasche:
        if "bag_size" in st.session_state:
            bag_size = st.session_state["bag_size"]
            st.write(f"Du hast eine Taschengröße ausgewählt: {bag_size}")
            bag_images = {
                    "Klein (5 kg)": "./images/klein.png",
                    "Mittel (10 kg)": "./images/mittel.png",
                    "Groß (15 kg)": "./images/gross.png",
                }
            st.image(bag_images.get(bag_size, ""), caption=bag_size, use_container_width=True)
        
        
        
        tasche_data = st.session_state.get("bag_size", "Keine Auswahl")
        st.write("Tasche:", tasche_data)
    with gegenstände:
        gegenstände_data = st.session_state.get("gegenstände_df", pd.DataFrame(columns=["Gegenstand", "Gewicht (kg)", "Nutzen"]))
        st.write("Gegenstände:")
        st.dataframe(gegenstände_data, hide_index=True)

    
    
    st.title("Auswahl und Erklärung der Algorithmen")

    # Container für Allgemeine Erklärung
    with st.container():
        titel, alignment, middle = st.columns(3)
        with alignment:
            st.subheader(":orange[Allgemeine Erklärung]")
        greedy, dp, gurobi = st.columns(3)
        with greedy:
            st.markdown(r"""
            #### Greedy-Algorithmus
            Der :orange[Greedy-Algorithmus] ist ein heuristischer Ansatz, der iterativ Entscheidungen trifft, die in jedem Schritt lokal optimal erscheinen. 
            Beim Knapsack-Problem bedeutet dies, dass der Algorithmus Gegenstände basierend auf einer bestimmten Strategie auswählt, wie z. B. dem höchsten Nutzen-Gewicht-Verhältnis (Effizienz), bis die Kapazität erschöpft ist.
            """)

        with dp:
            st.markdown(r"""
            #### Dynamische Programmierung
            Die :orange[Dynamische Programmierung] ist ein exakter Ansatz, der das Problem in kleinere Teilprobleme aufteilt und deren Lösungen speichert, 
            um Redundanzen zu vermeiden. Für das Knapsack-Problem wird eine Matrix aufgebaut, die mögliche Gewichtslimits und Gegenstandsauswahlen abdeckt.
            """)

        with gurobi:
            st.markdown(r"""
            #### Gurobi-Solver
            Der :orange[Gurobi-Solver] ist ein kommerzielles Tool für mathematische Optimierungsprobleme, das lineare, gemischt-ganzzahlige und quadratische Probleme löst. 
            Beim Knapsack-Problem wird ein gemischt-ganzzahliges lineares Programm (MILP) formuliert und gelöst.
            """)
    st.markdown("---")

    # Container für Mathematischen Hintergrund
    with st.container():
        titel, alignment, middle = st.columns(3)
        with alignment:
            st.subheader(":orange[Mathematischer Hintergrund]")
        greedy, dp, gurobi = st.columns(3)
        with greedy:
            st.markdown(r"""
            $$
            Effizienz = \frac{v_i}{w_i}
            $$
            Der Greedy-Algorithmus wählt in jedem Schritt das Element $$i$$, das diese Bedingung maximiert.
            """)

        with dp:
            st.markdown(r"""
            $$
            dp[i][w] = \max(dp[i-1][w],
            \\dp[i-1][w-w_i] + v_i)
            $$
            Diese Rekursionsbeziehung berechnet den maximal Nutzen.
            """)

        with gurobi:
            st.markdown(r"""
            $$
            \text{Maximiere:} \quad \sum_{i=1}^n v_i \cdot x_i
            $$
            $$
            \text{Nebenbedingung:} \quad \sum_{i=1}^n w_i \cdot x_i \leq W, \quad x_i \in \{0, 1\}
            $$
            Dabei sind $$x_i$$ binäre Variablen, die angeben, ob ein Gegenstand ausgewählt wurde.
            """)
    st.markdown("---")

    # Container für Vorteile
    with st.container():
        titel, alignment, middle = st.columns(3)
        with alignment:
            st.subheader(":orange[Vorteile]")
        greedy, dp, gurobi = st.columns(3)
        with greedy:
            st.markdown(r"""
            - Sehr schnell und effizient mit einer Laufzeit von $\mathcal{O}(n \log n)$.
            - Einfach zu implementieren und gut für große Datenmengen geeignet.
            - Liefert oft akzeptable Lösungen in kurzer Zeit.
            """)

        with dp:
            st.markdown(r"""
            - Liefert immer eine optimale Lösung für das klassische Knapsack-Problem.
            - Gut geeignet für kleine bis mittelgroße Probleme.
            """)

        with gurobi:
            st.markdown(r"""
            - Liefert die exakte optimale Lösung, auch für sehr komplexe Problemvarianten.
            - Sehr flexibel: Kann Nebenbedingungen und zusätzliche Constraints leicht integrieren.
            """)
    st.markdown("---")

    # Container für Nachteile
    with st.container():
        titel, alignment, middle = st.columns(3)
        with alignment:
            st.subheader(":orange[Nachteile]")
        greedy, dp, gurobi = st.columns(3)
        with greedy:
            st.markdown(r"""
            - Nicht optimal für das klassische Knapsack-Problem, da globale Wechselwirkungen ignoriert werden.
            - Funktioniert perfekt nur für spezielle Problemvarianten (z. B. das kontinuierliche Knapsack-Problem).
            """)

        with dp:
            st.markdown(r"""
            - Höherer Rechen- und Speicheraufwand: Laufzeit von $\mathcal{O}(n \cdot W)$, wobei $W$ die maximale Kapazität ist.
            - Nicht skalierbar für sehr große Probleme mit hohen Gewichtslimits.
            """)

        with gurobi:
            st.markdown(r"""
            - Hoher Rechenaufwand bei sehr großen Probleminstanzen.
            - Komplexität in der Einrichtung und Abhängigkeit von einer kommerziellen Lizenz.
            """)
    st.markdown("---")

    # Container für Typische Anwendungsfälle
    with st.container():
        titel, alignment, middle = st.columns(3)
        with alignment:
            st.subheader(":orange[Typische Anwendungsfälle]")
        greedy, dp, gurobi = st.columns(3)
        with greedy:
            st.markdown(r"""
            - Schnelle Näherungslösungen für Probleme, bei denen Genauigkeit nicht entscheidend ist.
            - Echtzeitanwendungen, bei denen Rechenzeit begrenzt ist.
            """)

        with dp:
            st.markdown(r"""
            - Probleme, bei denen Genauigkeit wichtiger ist als Rechenzeit.
            - Anwendungen in der Theorie und Forschung, um optimale Lösungen zu validieren.
            """)

        with gurobi:
            st.markdown(r"""
            - Industrielle Anwendungen mit hohen Genauigkeitsanforderungen (z. B. Logistik, Finanzwesen).
            - Problemlösungen, die mehrere komplexe Nebenbedingungen berücksichtigen müssen.
            """)
    st.markdown("---")

    # Auswahlbereich
    st.subheader(":orange[Wähle deinen Algorithmus aus]")
    Auswahltext = """
    Jetzt, da du die Unterschiede der drei Algorithmen kennst, kannst du auswählen, welchen Ansatz du für die Lösung deines Problems nutzen möchtest. 
    Wähle einen oder mehrere Algorithmen, um das Knapsack-Problem zu lösen, und vergleiche die Ergebnisse!
    """
    st.write(Auswahltext)
    
    greedy, dp, gurobi = st.columns(3)
    with greedy:
        if st.checkbox("Greedy-Algorithmus"):
            st.session_state["greedy"] = True
    with dp:
        dp = st.checkbox("Dynamische Programmierung")
    with gurobi:
        gurobi = st.checkbox("Gurobi-Solver")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Zurück"):
            navigate("Eingabemaske_Gegenstände", pages)
    with col2:
        if st.button("Weiter"):
            navigate("Ergebnismaske", pages)