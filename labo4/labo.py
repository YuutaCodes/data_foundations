import json
import pandas as pd


# Stap 1: Metadata verzamelen en toevoegen
df = pd.read_excel('Online Retail.xlsx')

print(df.head(5))

TYPES = {'i': 'int', 'f': 'float', 'M': 'datetime', 'O': 'string'}

meta = {
    "InvoiceNo": ("Factuurnummer", "hoog"),
    "StockCode": ("Productcode", "hoog"),
    "Description": ("Productomschrijving", "laag"),
    "Quantity": ("Aantal verkochte eenheden", "medium"),
    "InvoiceDate": ("Datum en tijdstip van de factuur", "medium"),
    "UnitPrice": ("Prijs per eenheid in pond sterling", "hoog"),
    "CustomerID": ("Unieke klantidentificatie", "medium"),
    "Country": ("Land van de klant", "laag"),
}

schema = {
    col: {
        "description": meta[col][0],
        "datatype": TYPES[df[col].dtype.kind],
        "importance": meta[col][1],
    }
    for col in meta
}

# Stap 2: Bouw een data catalogus

print("")
print("--- Data Catalogus ---")
print("")

with open('metadata.json', 'w', encoding='utf-8') as f:
    json.dump(schema, f, indent=2, ensure_ascii=False)

metadata = pd.read_json("metadata.json")
print(metadata)

## Search

def search(catalogus, importance=None, tekst=None):
   result = catalogus
   if importance:
       result = result[result["importance"] == importance]
   if tekst:
        result = result[result["description"].str.contains(tekst, case=False)]

   return result

print("")
print(search(metadata.T, importance="hoog"))
print("")
print(search(metadata.T, tekst="factuur"))

# Stap 3: Data lineage logboek
logboek = []

def log(step, action, columns, before, after):
    logboek.append({"step": step, "action": action, "columns": columns,
                    "rows_before": before, "rows_after": after, "rows_changed": abs(before - after) or after})

log("Origineel", "ingeladen", list(df.columns), len(df), len(df))

before = len(df)
df = df.drop_duplicates()
log("Duplicaten verwijderen", "gefilterd", list(df.columns), before, len(df))

df['total_sales'] = df['Quantity'] * df['UnitPrice']
log("total_sales toevoegen", "toegevoegd", ["total_sales"], len(df), len(df))

before = len(df)
df_filtered = df[df["Quantity"] > 10]
log("Filter Quantity > 10", "gefilterd", ["Quantity"], before, len(df_filtered))

print("")
print(pd.DataFrame(logboek).to_string())

# Stap 4: Data lineage visualiseren
import matplotlib.pyplot as plt
import networkx as nx

graph = nx.DiGraph()
labels = [f"{e['step']}\n{e['rows_after']:,} rijen" for e in logboek]
nx.add_path(graph, labels)
positions = {label: (i, 0) for i, label in enumerate(labels)}

plt.figure(figsize=(14, 3))
nx.draw(graph, positions, with_labels=True, node_shape="s", node_size=9000,
        node_color="lightsteelblue", font_size=9, arrowsize=20)
plt.title("Data lineage - Online Retail")
plt.margins(x=0.1)
plt.savefig("lineage.png", bbox_inches="tight", dpi=150)
plt.show()
