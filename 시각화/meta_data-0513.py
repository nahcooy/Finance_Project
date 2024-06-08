import pandas as pd
import matplotlib.pyplot as plt

# Assume the CSV file is named 'data.csv' and located in the current directory
# Replace 'filepath' with your actual file path if it's located elsewhere
filepath = 'Ideal_growth_dates.csv'

# Reading data from CSV
df = pd.read_csv(filepath)

# Converting 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Extracting year from the 'Date' column
df['Year'] = df['Date'].dt.year

# Plotting a histogram of the 'Year' column
plt.figure(figsize=(10, 6))
df['Year'].hist(bins=range(df['Year'].min(), df['Year'].max()+1), alpha=0.7, color='blue', edgecolor='black')
plt.title('Histogram of Years')
plt.xlabel('Year')
plt.ylabel('Frequency')
plt.grid(axis='y', alpha=0.75)
plt.show()
