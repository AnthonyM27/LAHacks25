from scholarly import scholarly
import networkx as nx
from pyvis.network import Network

# Example researchers
researchers = ["John Doe", "Jane Smith", "Alex Johnson"]

# Step 1: Create graph
G = nx.Graph()

# Step 2: Search researchers and add nodes
for name in researchers:
    search_query = scholarly.search_author(name)
    author = next(search_query)
    full_author = scholarly.fill(author, sections=['publications'])

    G.add_node(author['name'])

    for pub in full_author.get('publications', []):
        pub_filled = scholarly.fill(pub)
        co_authors = pub_filled.get('author', [])

        for coauthor in co_authors:
            if coauthor != author['name']:
                G.add_edge(author['name'], coauthor)

# Step 3: Visualize
net = Network(notebook=True)
net.from_nx(G)
net.show("research_collab.html")
