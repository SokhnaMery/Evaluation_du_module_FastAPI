import pandas as pd

data = pd.read_csv("questions.csv")
print (data)
print(data.head(10))

print(data.info())

print(data.describe())

print(data['subject'].unique())
