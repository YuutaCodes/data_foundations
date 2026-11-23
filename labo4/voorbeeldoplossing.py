import pandas as pd
import json
import networkx as nx
import matplotlib.pyplot as plt

# Stap 1: Laad de dataset in
df = pd.read_excel("Online Retail.xlsx")

# Stap 2: Metadata verzamelen en opslaan
# Metadata handmatig definiëren
metadata = {
    "InvoiceNo": {"description": "Factuurnummer", "datatype": "string", "importance": "hoog"},
    "StockCode": {"description": "Productcode", "datatype": "string", "importance": "hoog"},
    "Description": {"description": "Beschrijving van het product", "datatype": "string", "importance": "medium"},
    "Quantity": {"description": "Aantal verkochte eenheden", "datatype": "int", "importance": "medium"},
    "InvoiceDate": {"description": "Datum en tijd van transactie", "datatype": "datetime", "importance": "hoog"},
    "UnitPrice": {"description": "Prijs per eenheid van het product", "datatype": "float", "importance": "hoog"},
    "CustomerID": {"description": "Unieke ID van de klant", "datatype": "float", "importance": "medium"},
    "Country": {"description": "Land van de klant", "datatype": "string", "importance": "medium"}
}

# Metadata opslaan in een JSON-bestand
with open("metadata.json", "w") as f:
    json.dump(metadata, f, indent=4)

# Stap 3: Data catalogus weergeven
# Metadata inlezen en weergeven
metadata_df = pd.DataFrame(metadata).T  # Draai de dictionary om in een DataFrame
print("Data Catalogus:\n", metadata_df)

# Zoekfunctie voor de data catalogus
def search_catalog(importance_level):
    """Zoek kolommen op basis van het belangrijkheidsniveau."""
    result = metadata_df[metadata_df['importance'] == importance_level]
    return result

# Voorbeeld van zoekfunctie
print("Zoekresultaten voor 'hoog' belangrijkheidsniveau:\n", search_catalog("hoog"))

# Stap 4: Data lineage logboek en transformaties
# Transformatie 1: Verwijder duplicaten
df = df.drop_duplicates()

# Transformatie 2: Voeg kolom 'total_sales' toe
df['total_sales'] = df['UnitPrice'] * df['Quantity']

# Transformatie 3: Filter de records waar 'Quantity' > 10
df = df[df['Quantity'] > 10]

# Stap 5: Data lineage visualiseren met networkx en matplotlib
# Creëer een directed graph voor de data lineage
G = nx.DiGraph()

# Voeg knooppunten toe voor elke transformatiestap
G.add_node("Start")
G.add_node("Deduplication", label="Verwijder duplicaten")
G.add_node("Calculation", label="Bereken total_sales")
G.add_node("Filtering", label="Filter Quantity > 10")

# Voeg randen toe om de volgorde van de transformaties weer te geven
G.add_edges_from([
    ("Start", "Deduplication"),
    ("Deduplication", "Calculation"),
    ("Calculation", "Filtering")
])

# Plot de grafiek met networkx en matplotlib
plt.figure(figsize=(8, 6))
pos = nx.spring_layout(G)  # Kies een layout voor de grafiek
nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=10, font_weight="bold", arrows=True)
nx.draw_networkx_labels(G, pos, labels={node: G.nodes[node].get('label', node) for node in G.nodes})

plt.title("Data Lineage Visualisatie")
plt.show()

# Samenvatting van de data catalogus en visualisatie
print("\nSamenvatting van de data catalogus:\n", metadata_df)
print("\nEindstatus van de dataset na transformaties:\n", df.head())
