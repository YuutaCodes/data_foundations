import json
import pandas as pd
import seaborn

# Stap 1: Metadata verzamelen en toevoegen
df = pd.read_csv("Nashville_housing_data_2013_2016.csv")

## Beter beeld krijgen
print(df.head())
print(df.info())

## 56626 rijen en 31 kolommen
print(df.shape)

# Stap 2: identificeer master data

## mijn interpretatie zijn kerngegevens die uniek zijn voor een object, en deze data veranderd dus ook bijna niet
data_types = {
    "master_pand": ["Parcel ID", "Property Address", "Suite/ Condo   #", "Acreage", "Finished Area",
                    "Year Built", "Bedrooms", "Full Bath", "Half Bath", "Neighborhood", "image",
                    "Land Value", "Building Value", "Total Value"],
    "master_eigenaar": ["Owner Name", "Address"],
    "referentie": ["Land Use", "Tax District", "Property City", "City", "State",
                   "Foundation Type", "Exterior Wall", "Grade"],
    "transactie": ["Legal Reference", "Sale Date", "Sale Price", "Sold As Vacant",
                   "Multiple Parcels Involved in Sale"],
    "technisch": ["Unnamed: 0.1", "Unnamed: 0"],
}
print(json.dumps(data_types, indent=2))

# Stap 3: opschonen en harmoniseren van master data
## ik snap de vraag niet? als PropertyAddress ontbreekt maar OwnerAddress hetzelfde is?

print("Ontbrekende adressen voor:", df["Property Address"].isna().sum())

## Onthoud welke rijen leeg waren
was_leeg = df["Property Address"].isna()

## Aanvullen via hetzelfde perceel (zelfde Parcel ID = zelfde pand = zelfde adres)
df["Property Address"] = df["Property Address"].fillna(df.groupby("Parcel ID")["Property Address"].transform("first"))

## Aanvullen via eigenaarsadres (eigenaar woont meestal zelf in het pand)
df["Property Address"] = df["Property Address"].fillna(df["Address"])

print("Ontbrekende adressen na:", df["Property Address"].isna().sum())

print(df[was_leeg & df["Property Address"].notna()][["Parcel ID", "Property Address"]])

df["Owner Name"] = (
    df["Owner Name"]
    .str.upper()
    .str.strip()
    .str.replace(r"\s*,+\s*", ", ", regex=True)
    .str.replace(r"\s+", " ", regex=True)
)

## Adressen ook uniformiseren, anders lijkt "301 MYSTIC HILL  DR" een ander pand dan "301 MYSTIC HILL DR"
df["Property Address"] = df["Property Address"].str.strip().str.replace(r"\s+", " ", regex=True)
df["Address"] = df["Address"].str.strip().str.replace(r"\s+", " ", regex=True)

## 1. Volledig dubbele rijen
zonder_index = df.columns.drop(data_types["technisch"])
print("Dubbele rijen:", df.duplicated(subset=zonder_index).sum())
df = df.drop_duplicates(subset=zonder_index)
print("Rijen over:", len(df))

## 2. Master data pand
pand = df[data_types["master_pand"]]
print("Pand-rijen voor:", len(pand))
pand = pand.drop_duplicates(subset="Parcel ID")
print("Pand-rijen na:", len(pand))

## 3. Master data eigenaar
eigenaar = df[data_types["master_eigenaar"]].dropna(subset=["Owner Name"])
print("Eigenaar-rijen voor:", len(eigenaar))
eigenaar = eigenaar.drop_duplicates()
print("Eigenaar-rijen na:", len(eigenaar))

df["Sale Date"] = pd.to_datetime(df["Sale Date"], format="%Y-%m-%d", errors="coerce")
df = df.dropna(subset=["Sale Date"])
print(df["Sale Date"])

eigenaar_kolommen = ["Owner Name", "Address", "City", "State"]
master_owners = df[eigenaar_kolommen].dropna(subset=["Owner Name"]).drop_duplicates()
master_owners["Owner ID"] = range(1, len(master_owners) + 1)
print(master_owners.head())

df = df.merge(master_owners, on=eigenaar_kolommen, how="left")
print(df[["Parcel ID", "Sale Date", "Owner ID", "Owner Name"]].dropna().head())

print(df.duplicated().sum())

print(df.isnull().sum())
print(df.isnull().mean())
seaborn.heatmap(df.isnull())