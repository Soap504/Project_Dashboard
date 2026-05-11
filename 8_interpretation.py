import streamlit as st


def render_interpretation():
    st.header("Final Overview & Project Interpretation")

    st.markdown("""
    This dashboard is designed to explore the structure of an institutional email network and answer key research questions 
    about communication patterns, centrality, and connectivity.
    """)

    st.markdown("""
    ## **Key Takeaways**
    **Question 1: Do communication communities align with department structure?**
    - The email network only partially follows departmental structure
    - Communication is not strictly limited within departments
    
    The institution's email communication network structure suggests that email communication network does follow departmental structure.
    However, departments don't completely make up how the email communication network is shaped as most communications are cross-department
    instead of within. For most departments within the institution, they seem to follow departmental structure, but there are some 
    departments in which the communications outside of their department is more prominent than the communications within. This suggests
    that within a large institution, there may exist more than one form of communication, so just email communications alone won't fully
    capture departmental structure. The higher percentage of cross-department communications compared to within department communications 
    also suggests that email communications might be a more formal way of communicating with other departments that are harder to reach, 
    compared to people within the same departments where communication could be through more informal means.
            
    
    **Question 2: Who appears structurally central?**
    - Node 160 has a much higher centrality score than anyone else
    - Centrality score is very high with a small group of select members

    From the centrality analysis, we can see that Node 160 is by far the most central node within the institution's email network. 
    This suggests that Node 160 is an important figure within the network with a high ranking compared to the rest. The network also
    shows that there are not many nodes with a high centrality score. This means that the network is defined by a small group of important
    figures who manages most communications within the network.
    
    **Question 3: Which individuals may act as bridges across groups?**
    - Node 160 has a much higher bridge score than anyone else
    - A small number of nodes act as **bridges**, connecting different parts of the network 
                
    From the bridge calculations, we can see that node 160 is also by far the individual that connects most of the network together. 
    This means that node 160 is an important mediator of how communications are being conducted throughout the network. Besides from 
    node 160, there are a small number of nodes that also has a relatively high score compared to the rest. These people are important
    as they help connect the email communication network together between everyone within it. 
                
    ## **Final Takeaways**
    An institution's email communication network structure suggests that email communication network partially follows departmental structure. 
    More prominent cross-department communication suggests email communications might be a more formal way of communicating with other departments
    while within department communications might be through other informal means. Node 160 is a key actor within the research institution as 
    someone who is both central and connects the most people within the network. This suggests that node 160 could be the CEO of the research
    institution or some position of that high status. Some nodes like nodes 64 and 166 have high bridge scores, but low centrality scores which suggests
    that these people might be researchers who are involved with a lot of collaborations and cross-department researches. Although they might connect 
    to a lot of people, they're not central actors within the network. On the other hand, nodes that are high in centality score suggests a higher position
    within the institution. This mostly suggests that these people are department managers or someone of that status.

    ## **Challenges & Limitations**
    1. Dataset is anonymized
        - Since our dataset is anonymized, we can't actually identify who these key actors within our network. We can only infer from what our analysis suggests. 
    2. Edges only show existence of communication, not frequency or strength  
        - We could only analyze our dataset based on email comunications between individuals and not how frequent emails are exchanged between individuals. If we were able
        to analyze how often email communications are between individuals, we might be see more apparent departmental structure because just because there's reciprocity 
        between two nodes doesn't mean the communication is maintained. 
    3. Network analysis is limited to structure, not intensity of interactions
        - Due to the limitation of our dataset not showing frequency of communication or strength of relationships, we can only analyze the network structure and not how 
        strong individual connections might be which could suggest different community structure.  
    """)


