import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("austpop.csv")

## Zonder Aust -> geen staat maar het totaal
states = ["NSW", "Vic", "Qld", "SA", "WA", "Tas", "NT", "ACT"]

wide = df.set_index("year")[states]

# Bivariate analyse

year = df["year"]
vic = df["Vic"]

print("Correlatiecoëfficiënt van Victoria en jaar: " + str(year.corr(vic)))

plt.scatter(year, vic)
plt.xlabel("Jaar")
plt.ylabel("Bevolking Victoria (duizendtallen)")
plt.title("Victoria: bevolking per jaar")
plt.show()

print("\nCorrelatiematrix van alle staten (niveaus):")
print(wide.corr().round(3))

# Tijdreeksanalyse

## groei (relatief, per decennium)
growth = wide.pct_change()
print("\nRelatieve groei per decennium:")
print(growth.round(3))

wide.plot(figsize=(10, 6))
plt.yscale("log")
plt.ylabel("Population in thousands (log scale)")
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.show()

print("\nCorrelatiematrix van de groeipercentages:")
print(growth.corr().round(3))

# Boxplots: groeipercentages

growth.dropna().boxplot(figsize=(10, 6))
plt.ylabel("Relatieve groei per decennium")
plt.title("Verdeling van de groei per staat")
plt.tight_layout()
plt.show()

# Stap 3: gegevens verrijken

aandeel = wide.div(df["Aust"].values, axis=0) * 100
print("\nAandeel van elke staat in de totale bevolking (%):")
print(aandeel.round(2))

toename = wide.diff()
print("\nAbsolute toename per decennium (duizendtallen):")
print(toename)

aandeel.plot(figsize=(10, 6))
plt.ylabel("Aandeel in totale bevolking (%)")
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.show()

# Stap 4: interpretatie en conclusies

# INTERPRETATIE

# 1. Correlaties
#    Op niveaus correleert alles met alles rond 0.99. elke staat
#    groeit monotoon van 1917 tot 1997, dus ze hebben een gelijke opwaartse
#    trend.

# 2. Trends in bevolkingsgroei
#    De absolute aantallen stijgen overal, maar de groei per decennium piekt rond
#    1947-1967 (naoorlogse babyboom en immigratie) en vlakt daarna af. In het
#    lijndiagram met logaritmische y-as is dat zichtbaar als een afnemende helling.

# 3. Groeien de staten synchroon
#    Deels. NSW, Vic, SA en ACT groeien duidelijk samen: als de ene een goed
#    decennium heeft, heeft de andere dat ook.
#    Qld volgt maar half (rond 0.5) en NT doet volledig zijn eigen ding. Er is dus niet een enkele
#    Australische trend, maar een groep die samen beweegt en een paar
#    buitenbeentjes

# 4. Structurele verschillen
#    Sommige staten groeien veel sneller dan andere. ACT ging van 3 naar 310
#    (103 keer zo groot) en NT van 5 naar 187 (37 keer). NSW werd maar 3.3 keer
#    zo groot en Tasmanie 2.5 keer: dat is de traagste.
#    ACT en NT begonnen heel klein, dus een kleine toename is daar
#    meteen een groot percentage. In absolute aantallen blijft NSW veruit de
#    grootste staat.
