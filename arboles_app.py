import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")

st.title("Tree Generator and Visualizer")

# Sidebar for variable configuration
st.sidebar.header("Configuration")

# Input for partidas (initial points)
partidas_input = st.sidebar.text_input("Initial Points (comma-separated)", "1,2,3,4,5,6")
partidas = [int(x.strip()) for x in partidas_input.split(",")]

# Input for pos_2 (second level)
pos_2_input = st.sidebar.text_input("Second Level (comma-separated)", "A,B,C")
pos_2 = [x.strip() for x in pos_2_input.split(",")]

# Input for fin (final level)
fin_input = st.sidebar.text_input("Final Level (comma-separated)", "D,E,F")
fin = [x.strip() for x in fin_input.split(",")]

# Generate all combinations
results = []
for inicio in partidas:
    for p2 in pos_2:
        for f in fin:
            results.append({
                'Initial': inicio,
                'Second': p2,
                'Final': f
            })

# Convert to DataFrame
df = pd.DataFrame(results)

# Display the results
st.header("Generated Combinations")
st.dataframe(df)

# Tree visualization
st.header("Tree Visualization")

# Select initial point for visualization
selected_initial = st.selectbox(
    "Select initial point to visualize",
    options=partidas
)

# Create a graph for the selected initial point
G = nx.DiGraph()

# Add nodes and edges for the selected initial point
G.add_node(str(selected_initial), level=0)

for p2 in pos_2:
    G.add_node(f"{selected_initial}-{p2}", level=1)
    G.add_edge(str(selected_initial), f"{selected_initial}-{p2}")
    
    for f in fin:
        G.add_node(f"{selected_initial}-{p2}-{f}", level=2)
        G.add_edge(f"{selected_initial}-{p2}", f"{selected_initial}-{p2}-{f}")

# Create the visualization
plt.figure(figsize=(20, 10))

# Create hierarchical layout
pos = {}
# Position initial node
pos[str(selected_initial)] = np.array([0, 0])

# Position second level nodes
for i, p2 in enumerate(pos_2):
    y_pos = (i - (len(pos_2)-1)/2) * 3  # Increased vertical spacing
    pos[f"{selected_initial}-{p2}"] = np.array([4, y_pos])

# Position final level nodes
for i, p2 in enumerate(pos_2):
    for j, f in enumerate(fin):
        y_pos = (i - (len(pos_2)-1)/2) * 3 + (j - (len(fin)-1)/2) * 0.8
        pos[f"{selected_initial}-{p2}-{f}"] = np.array([8, y_pos])

# Draw nodes with different colors for each level
node_colors = []
for node in G.nodes():
    if G.nodes[node]['level'] == 0:
        node_colors.append('lightblue')
    elif G.nodes[node]['level'] == 1:
        node_colors.append('lightgreen')
    else:
        node_colors.append('lightpink')

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                      node_size=4000, alpha=0.7)

# Draw edges with arrows
nx.draw_networkx_edges(G, pos, edge_color='gray', 
                      arrows=True, arrowsize=30, width=3)

# Draw labels with larger font
nx.draw_networkx_labels(G, pos, font_size=18, font_weight='bold')

plt.title(f"Tree Structure for Initial Point {selected_initial}", fontsize=24, pad=20)

# Add level labels with larger font and adjusted positions
plt.text(-1, 0, "Initial", fontsize=20, fontweight='bold')
plt.text(2, 0, "Second Level", fontsize=20, fontweight='bold')
plt.text(6, 0, "Final Level", fontsize=20, fontweight='bold')

# Display the plot in Streamlit
st.pyplot(plt)

# Add some statistics
st.header("Statistics")
st.write(f"Total number of combinations: {len(df)}")
st.write(f"Number of unique initial points: {len(partidas)}")
st.write(f"Number of second level options: {len(pos_2)}")
st.write(f"Number of final level options: {len(fin)}") 