import streamlit as st
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# Default distances between towns as edges in a graph
def get_default_edges():
    return [
        ('Chicago', 'McLain', 40), ('Chicago', 'Aurora', 60), ('Chicago', 'Parker', 50),
        ('McLain', 'Aurora', 10), ('McLain', 'Smallville', 70),
        ('Aurora', 'Parker', 20), ('Aurora', 'Smallville', 55), ('Aurora', 'Farmer', 40),
        ('Parker', 'Farmer', 50),
        ('Smallville', 'Farmer', 10), ('Smallville', 'Bayview', 60),
        ('Farmer', 'Bayview', 80)
    ]

st.title("🚗 Shortest Route from Chicago to Bayview")

st.sidebar.header("🔧 Customize Weights")

# Editable distance table
edge_df = pd.DataFrame(get_default_edges(), columns=['From', 'To', 'Distance'])
edited_df = st.sidebar.data_editor(edge_df, num_rows="dynamic", key="edit_distances")

# Graph generation
g = nx.DiGraph()
for _, row in edited_df.iterrows():
    g.add_edge(row['From'], row['To'], weight=row['Distance'])

# Select cost type
cost_type = st.selectbox("Select what the weights represent:",
                         ["Miles", "Cost in Dollars", "Time in Minutes"])

# Shortest path
try:
    path = nx.dijkstra_path(g, 'Chicago', 'Bayview', weight='weight')
    distance = nx.dijkstra_path_length(g, 'Chicago', 'Bayview', weight='weight')
    st.success(f"Shortest Path from Chicago to Bayview ({cost_type}): {' ➜ '.join(path)}")
    st.write(f"**Total {cost_type}: {distance}**")
except nx.NetworkXNoPath:
    st.error("No valid path from Chicago to Bayview based on current graph.")

# Visualize the graph
st.subheader("🗺️ Town Network Chart")
fig, ax = plt.subplots()
pos = nx.spring_layout(g, seed=42)
nx.draw(g, pos, with_labels=True, node_color='lightblue', node_size=1500, font_size=10, ax=ax)
labels = nx.get_edge_attributes(g, 'weight')
nx.draw_networkx_edge_labels(g, pos, edge_labels=labels, ax=ax)
st.pyplot(fig)

# Download editable data
csv = edited_df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Distance Table as CSV", csv, "chicago_to_bayview_distances.csv", "text/csv")

# Show adjacency matrix
st.subheader("📋 Adjacency Table")
nodes = sorted(set(edited_df['From']) | set(edited_df['To']))
mat = pd.DataFrame(index=nodes, columns=nodes)
for _, row in edited_df.iterrows():
    mat.at[row['From'], row['To']] = row['Distance']
st.dataframe(mat.fillna("--"))
