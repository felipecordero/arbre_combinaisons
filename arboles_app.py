import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from translations import LANGUAGES

# Set default theme to light
st.set_page_config(
    page_title="Tree Generator and Visualizer",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Custom CSS for kid-friendly styling
st.markdown("""
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 20px;
        padding: 10px 20px;
        font-size: 18px;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #4CAF50;
    }
    .stSelectbox>div>div>select {
        border-radius: 10px;
        border: 2px solid #4CAF50;
    }
    h1 {
        color: #2E7D32;
        font-size: 3em !important;
        text-align: center;
        padding: 20px;
    }
    h2 {
        color: #388E3C;
        font-size: 2em !important;
        padding: 15px;
    }
    h3 {
        color: #43A047;
        font-size: 1.5em !important;
        padding: 10px;
    }
    /* Make metric labels larger */
    .stMetric label {
        font-size: 1.2em !important;
        font-weight: bold !important;
    }
    /* Style the metric container */
    .stMetric {
        padding: 10px;
        border-radius: 10px;
        background-color: #E8F5E9;
    }
    </style>
    """, unsafe_allow_html=True)

# Language selector in sidebar with emoji
selected_language = st.sidebar.selectbox(
    "🌍 Language / Langue / Idioma / Lingua",
    options=list(LANGUAGES.keys()),
    index=0
)

# Get translations
t = LANGUAGES[selected_language]

# Main title with emoji
st.title(f"🌳 {t['title']} 🌳")

# Sidebar for variable configuration with emoji
st.sidebar.header(f"⚙️ {t['config_header']}")

# Input for partidas (initial points) with emoji
partidas_input = st.sidebar.text_input(f"🔢 {t['initial_points']}", "1,2,3,4,5,6")
partidas = [int(x.strip()) for x in partidas_input.split(",")]

# Input for pos_2 (second level) with emoji
pos_2_input = st.sidebar.text_input(f"🔤 {t['second_level']}", "A,B,C")
pos_2 = [x.strip() for x in pos_2_input.split(",")]

# Input for fin (final level) with emoji
fin_input = st.sidebar.text_input(f"🎯 {t['final_level']}", "D,E,F")
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

# Create two columns for the main content
col_table, col_tree = st.columns([1, 1])

# Display the results with emoji in the left column
with col_table:
    st.header(f"📊 {t['combinations_header']}")
    st.dataframe(df.style.set_properties(**{
        'background-color': '#E8F5E9',
        'color': '#1B5E20',
        'border': '1px solid #A5D6A7'
    }))

# Tree visualization with emoji in the right column
with col_tree:
    st.header(f"🎨 {t['tree_visualization']}")

    # Select initial point for visualization with emoji
    selected_initial = st.selectbox(
        f"🎯 {t['select_initial']}",
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

    # Create the visualization with a more colorful style
    plt.figure(figsize=(15, 10))  # Adjusted size for column
    plt.style.use('default')  # Use default style as base

    # Set a light background
    plt.rcParams['figure.facecolor'] = '#f0f2f6'
    plt.rcParams['axes.facecolor'] = '#f0f2f6'

    # Create hierarchical layout
    pos = {}
    # Position initial node
    pos[str(selected_initial)] = np.array([0, 0])

    # Position second level nodes
    for i, p2 in enumerate(pos_2):
        y_pos = (i - (len(pos_2)-1)/2) * 3
        pos[f"{selected_initial}-{p2}"] = np.array([4, y_pos])

    # Position final level nodes
    for i, p2 in enumerate(pos_2):
        for j, f in enumerate(fin):
            y_pos = (i - (len(pos_2)-1)/2) * 3 + (j - (len(fin)-1)/2) * 0.8
            pos[f"{selected_initial}-{p2}-{f}"] = np.array([8, y_pos])

    # Draw nodes with more vibrant colors
    node_colors = []
    for node in G.nodes():
        if G.nodes[node]['level'] == 0:
            node_colors.append('#4CAF50')  # Green
        elif G.nodes[node]['level'] == 1:
            node_colors.append('#2196F3')  # Blue
        else:
            node_colors.append('#FF9800')  # Orange

    # Draw nodes with larger size and better styling
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                          node_size=4000, alpha=0.8,  # Slightly smaller nodes
                          edgecolors='white', linewidths=2)

    # Draw edges with better styling
    nx.draw_networkx_edges(G, pos, edge_color='#757575', 
                          arrows=True, arrowsize=30, width=3,
                          alpha=0.6)

    # Draw labels with better styling
    nx.draw_networkx_labels(G, pos, font_size=18, font_weight='bold',
                           font_color='white')

    # Remove axis
    plt.axis('off')

    plt.title(f"🌳 Tree Structure for Initial Point {selected_initial} 🌳", 
             fontsize=20, pad=20, color='#2E7D32')

    # Add level labels with better styling
    plt.text(-1, 0, f"🌱 {t['initial_label']}", fontsize=18, fontweight='bold', color='#2E7D32')
    plt.text(2, 0, f"🌿 {t['second_label']}", fontsize=18, fontweight='bold', color='#1565C0')
    plt.text(6, 0, f"🍃 {t['final_label']}", fontsize=18, fontweight='bold', color='#E65100')

    # Display the plot in Streamlit
    st.pyplot(plt)

# Add statistics with emojis below both columns
st.header(f"📈 {t['statistics']}")
col1, col2 = st.columns(2)
with col1:
    st.metric(f"🔢 {t['total_combinations']}", len(df))
    st.metric(f"🎯 {t['unique_initial']}", len(partidas))
with col2:
    st.metric(f"🔤 {t['second_options']}", len(pos_2))
    st.metric(f"🎯 {t['final_options']}", len(fin)) 