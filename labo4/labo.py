import json
import pandas as pd


# Stap 1: Metadata verzamelen en toevoegen
df = pd.read_excel('Online Retail.xlsx')

print(df.head(5))

TYPES = {'i': 'int', 'f': 'float', 'M': 'datetime', 'O': 'string'}

meta = {
    "InvoiceNo": ("Factuurnummer", "hoog"),
    "StockCode": ("Productcode", "hoog"),
    "Quantity": ("Aantal verkochte eenheden", "medium"),
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

def log(step, columns, rows):
    logboek.append({
        "step": step,
        "columns": columns,
        "rows": rows
    })

print("")
print("Total rows before de-duplication:" + str(len(df)))
log(1, [], len(df))

print("")
lenBefore = len(df)
df = df.drop_duplicates()
print("Total rows after de-duplication:" + str(len(df)))

log(2, [], lenBefore - len(df))

print("")
print("Adding total_sales column")
df['total_sales'] = df['Quantity'] * df['UnitPrice']
print(df.head(5))

log(3, ['total_sales'], len(df))

print("")
print("filter quantity > 10")
lenBefore = len(df)
dfFilter = df[df["Quantity"] > 10]
print(dfFilter.head(5))

log(4, ["Quantity"], lenBefore - len(dfFilter))

print("")
print(logboek)