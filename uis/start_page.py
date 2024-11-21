import streamlit as st 
from navigate import navigate



def start_page():
    st.title("Eine Einführung in das :orange[Knapsack-Problem]")
    
    st.header("Was ist das :orange[Knapsack-Problem]?")
    
    Allgemeine_Erklärung = r"""
     
    Das **:orange[Knapsack-Problem]** ist ein klassisches Problem aus der kombinatorischen Optimierung
    und der theoretischen Informatik. Es befasst sich mit der Frage, wie eine begrenzte Ressource –
    in diesem Fall der Platz in einem Rucksack – optimal genutzt werden kann, um den Nutzen zu maximieren.

    Formal lässt sich das Problem wie folgt beschreiben: Gegeben ist eine Menge von
    Gegenständen $n$, wobei jeder Gegenstand $i$ durch zwei Werte charakterisiert wird:
    $$
    w_i: \text{Das Gewicht des Gegenstands} \\
    v_i: \text{Der Nutzen des Gegenstands}
    $$
    
    Zusätzlich gibt es eine Kapazitätsgrenze $W$, die der Rucksack nicht überschreiten darf. 
        
    Ziel ist es, eine Auswahl von Gegenständen $S \subseteq \{1, \dots, n\}$ so zu treffen, dass die folgende Bedingung $\sum_{i \in S} w_i \leq W$ erfüllt wird
    und der Gesamtnutzen $\max \sum_{i \in S} v_i$ maximiert wird. 
    Das Problem hat eine hohe Relevanz in der Praxis und gehört zu den NP-schweren Problemen, was bedeutet, dass es keine effiziente Lösung für alle Eingabefälle gibt.
    Dennoch können Approximationsalgorithmen und heuristische Methoden in vielen Szenarien effektive Lösungen liefern.
    """
    st.write(Allgemeine_Erklärung)
    
    st.header("Warum ist das :orange[Knapsack-Problem] relevant?")
    
    Relevanz = """
    Das :orange[Knapsack-Problem] ist nicht nur ein spannendes Gedankenspiel, sondern hat auch 
    zahlreiche praktische Anwendungen:
    - **Logistik**: Optimale Beladung von Transportfahrzeugen.
    - **Finanzen**: Auswahl des besten Investmentportfolios.
    - **Fertigungsplanung**: Optimierung der Produktionsprozesse und Ressourcenzuweisung.
    
    In vielen Bereichen der Wissenschaft und Technik hilft das :orange[Knapsack-Problem] 
    bei der Lösung komplexer Herausforderungen.
    """
    st.write(Relevanz)
    
    st.header("Wie funktioniert diese App?")
    
    Funktionsweise = """
    Willkommen zu meinem Stand! Ihr seht hier einen 
    Rucksack und verschiedene Gegenstände, die ihr in den Rucksack packen könnt. 

    Jeder Gegenstand hat ein Gewicht, aber den Nutzen schätzt ihr selbst ein! Euer Ziel ist es, 
    den Rucksack effizient zu packen, basierend auf eurer Gewicht-Nutzen-Bewertung.
    
    
    Während ihr packt, merkt ihr vielleicht, dass es nicht leicht ist, die optimale Auswahl zu treffen. 
    Hier kommt meine App ins Spiel:
    - Sie berechnet das :orange[Knapsack-Problem] basierend auf euren Bewertungen mithilfe verschiedener Algorithmen.
    - Ihr seht, wie sich eine datengestützte Lösung von der intuitiven Auswahl unterscheidet.
    
    Probiert es aus und entdeckt, wie datenbasierte Entscheidungen zu besseren Ergebnissen führen!
    """
    st.write(Funktionsweise)
        
    
    
    
    
    
    
    
    
    
    if st.button("Weiter"):
        navigate("Eingabemaske")
        
        

