import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('investment_simulation_results.csv')

print(df['Return Rate'])
print("~~~~~~~~~~~~~~~`")
print(df['Return Rate'].mean())
print(df['Return Rate'].max())
print(df['Return Rate'].min())

# 히스토그램 시각화
plt.figure(figsize=(10, 6))
bin_edges = np.arange(start=df['Return Rate'].min(), stop=df['Return Rate'].max() + 1, step=1)  # 1% 단위로 구간 설정
plt.hist(df['Return Rate'], bins=bin_edges, color='blue', edgecolor='black')
plt.title('Histogram of Return Rates')
plt.xlabel('Return Rate (%)')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()