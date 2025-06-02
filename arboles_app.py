import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.graph_objects as go
from translations import LANGUAGES
from styles import CUSTOM_CSS


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


# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Set seaborn style - using white background without grid
sns.set_theme(style="white", context="notebook", font_scale=1.2)
sns.set_palette("husl")  # Use seaborn's color palette


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

    # Create tabs for different visualizations
    tab1, tab2 = st.tabs(["Matplotlib", "Plotly"])

    with tab1:
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

        # Create the visualization with seaborn styling
        plt.figure(figsize=(15, 10))
        
        # Set a light background
        plt.rcParams['figure.facecolor'] = '#f0f2f6'
        plt.rcParams['axes.facecolor'] = '#f0f2f6'

        # Use seaborn's color palette for nodes
        node_colors = []
        for node in G.nodes():
            if G.nodes[node]['level'] == 0:
                node_colors.append(sns.color_palette("husl", 3)[0])  # First color
            elif G.nodes[node]['level'] == 1:
                node_colors.append(sns.color_palette("husl", 3)[1])  # Second color
            else:
                node_colors.append(sns.color_palette("husl", 3)[2])  # Third color

        # Create hierarchical layout
        pos = {}
        # Position initial node
        pos[str(selected_initial)] = np.array([0, 0])

        # Position second level nodes
        for i, p2 in enumerate(pos_2):
            y_pos = (i - (len(pos_2)-1)/2) * 4
            pos[f"{selected_initial}-{p2}"] = np.array([4, y_pos])

        # Position final level nodes with better spacing
        for i, p2 in enumerate(pos_2):
            for j, f in enumerate(fin):
                y_pos = (i - (len(pos_2)-1)/2) * 4 + (j - (len(fin)-1)/2) * 1.2
                pos[f"{selected_initial}-{p2}-{f}"] = np.array([8, y_pos])

        # Draw nodes with larger size and better styling
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                              node_size=6000, alpha=0.8,
                              edgecolors='white', linewidths=2)

        # Draw edges with better styling
        nx.draw_networkx_edges(G, pos, edge_color='#757575', 
                              arrows=True, arrowsize=30, width=3,
                              alpha=0.6)

        # Draw labels with better styling and larger font
        nx.draw_networkx_labels(G, pos, font_size=22, font_weight='bold',
                               font_color='white')

        # Remove axis and any remaining grid lines
        plt.axis('off')
        plt.grid(False)

        plt.title(f"Tree Structure for Initial Point {selected_initial}", 
                 fontsize=20, pad=20, color='#2E7D32')

        # Add level labels with simple text, moved more to the left and larger font
        plt.text(-2, 0, t['initial_label'], fontsize=22, fontweight='bold', color='#2E7D32')
        plt.text(1, 0, t['second_label'], fontsize=22, fontweight='bold', color='#1565C0')
        plt.text(5, 0, t['final_label'], fontsize=22, fontweight='bold', color='#E65100')

        # Display the plot in Streamlit
        st.pyplot(plt)

    with tab2:
        # Create a new graph for Plotly
        G_plotly = nx.DiGraph()

        # Add nodes and edges
        G_plotly.add_node(str(selected_initial), level=0)
        for p2 in pos_2:
            G_plotly.add_node(f"{selected_initial}-{p2}", level=1)
            G_plotly.add_edge(str(selected_initial), f"{selected_initial}-{p2}")
            for f in fin:
                G_plotly.add_node(f"{selected_initial}-{p2}-{f}", level=2)
                G_plotly.add_edge(f"{selected_initial}-{p2}", f"{selected_initial}-{p2}-{f}")

        # Create edge trace
        edge_x = []
        edge_y = []
        for edge in G_plotly.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='#757575'),
            hoverinfo='none',
            mode='lines+markers+text',
            marker=dict(size=10),
            textposition="middle center"
        )

        # Create node traces for each level
        node_traces = []
        colors = ['#2E7D32', '#1565C0', '#E65100']  # Green, Blue, Orange

        for level in range(3):
            node_x = []
            node_y = []
            node_text = []
            for node in G_plotly.nodes():
                if G_plotly.nodes[node]['level'] == level:
                    x, y = pos[node]
                    node_x.append(x)
                    node_y.append(y)
                    node_text.append(node)

            node_trace = go.Scatter(
                x=node_x, y=node_y,
                mode='markers+text',
                hoverinfo='text',
                text=node_text,
                textposition="middle center",
                marker=dict(
                    size=50,
                    color=colors[level],
                    line=dict(width=2, color='white')
                ),
                textfont=dict(size=20, color='white')
            )
            node_traces.append(node_trace)

        # Create the figure
        fig = go.Figure(data=[edge_trace] + node_traces,
                       layout=go.Layout(
                           title=dict(
                               text=f"Tree Structure for Initial Point {selected_initial}",
                               font=dict(size=20, color='#2E7D32')
                           ),
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=20, l=5, r=5, t=40),
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           plot_bgcolor='#f0f2f6'
                       ))

        # Add level labels
        fig.add_annotation(x=-2, y=0, text=t['initial_label'], showarrow=False, font=dict(size=22, color='#2E7D32'))
        fig.add_annotation(x=1, y=0, text=t['second_label'], showarrow=False, font=dict(size=22, color='#1565C0'))
        fig.add_annotation(x=5, y=0, text=t['final_label'], showarrow=False, font=dict(size=22, color='#E65100'))

        st.plotly_chart(fig, use_container_width=True)

# Add statistics with emojis below both columns
st.header(f"📈 {t['statistics']}")
col1, col2 = st.columns(2)
with col1:
    st.subheader(f"🔢 {t['total_combinations']}")
    st.write(f"## {len(df)}")
    st.subheader(f"🎯 {t['unique_initial']}")
    st.write(f"## {len(partidas)}")
with col2:
    st.subheader(f"🔤 {t['second_options']}")
    st.write(f"## {len(pos_2)}")
    st.subheader(f"🎯 {t['final_options']}")
    st.write(f"## {len(fin)}") 