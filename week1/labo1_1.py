import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('austpop.csv')

# Bivariate analyse

year = df['year']
vic = df['Vic']

print("Correlatiecoëfficiënt van New South Wales en jaar: " + str(year.corr(vic)))

plt.scatter(year, vic)
plt.show()

matrix = df.corr()
print("Correlatiematrix van alle staten: ")
print(matrix)

# Tijdreeksanalyse
## Zonder Aust, geen state
states = ['NSW', 'Vic', 'Qld', 'SA', 'WA', 'Tas', 'NT', 'ACT']

wide = df.set_index('year')[states]

## growth (relatief, per decennium)
growth = wide.pct_change()
print(growth.round(3))

wide.plot(figsize=(10, 6))
plt.yscale('log')
plt.ylabel('Population in thousands (log scale)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Boxplots

verdeling = df.set_index('year')[states]


plt.boxplot(verdeling)
plt.show()