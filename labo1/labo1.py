import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('austpop.csv')

print("Average of Australian population: " + str(df["Aust"].mean()))

print("Median of Australian population: " + str(df["Aust"].median()))

print("Modus of Australian population: " + str(df["Aust"].mode()))

print("Standard deviation of Australian population: " + str(df["Aust"].std()))

Q1 = df["Aust"].quantile(0.25)
Q3 = df["Aust"].quantile(0.75)

IQR = Q3 - Q1

print("Interquartile range of Australian population: " + str(IQR))

df["Aust"].hist(bins=8)
plt.show()

df.boxplot(["Aust"])
plt.show()