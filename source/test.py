import pandas as pd 

names = ['RACE', 'NUM', 'PP', 'ODDS', 'M/L', 'RUNNER', 'AGE', 'GENDER', 'BREED', 'TRAINER', 'JOCKEY']

race_data = pd.read_csv('wp_output_clean.csv', names=names)

# print(type(race_data))
# print(type(result_data))

# print(race_data)

df = pd.DataFrame(race_data)

# # print(df)


print(df['RUNNER'])

names1 = ['column 1', 'column 2', 'column 3', 'column 4', 'column 5', 'column 5', 'column 6']

# print(result_data)

result_data = pd.read_csv('race: 1.csv', names=names)

# result_data = pd.read_csv('race: 1.csv')
print(result_data)

# print(result_data.head(1))
# print(result_data.head(3))

# race_data.columns = ['RACE', 'NUM', 'PP', 'ODDS', 'M/L', 'RUNNER', 'AGE', 'GENDER', 'BREED', 'TRAINER', 'JOCKEY']


