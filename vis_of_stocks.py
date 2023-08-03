import pandas as pd
from matplotlib import pyplot as plt

# Import of data
df = pd.read_csv('close_data.csv')
print(df)
tickers = ['AAPL', 'BYDDF', 'EONGY', 'LNVGF', 'NIO', 'PLUN.F', 'TSLA', 'TKA.DE', 'XIACF']
stock_buy_price = [110.96, 24.95, 11.47, 1.419, 47.81, 45.544, 159.95, 6.799474, 1.6198]

# Calculate percentage change
stock_close_price = df.iloc[-1, 1:].tolist()
percentage_change = [(close_price - buy_price) / buy_price * 100 for close_price, buy_price in zip(stock_close_price, stock_buy_price)]


# Visualization of Stocks
plt.figure(figsize = (10,6))
bars = plt.bar(tickers, percentage_change, color = 'tab:blue')


bar_labels = [f"{ticker} ({change:.2f}%)" for ticker, change in zip(tickers, percentage_change)]
bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:gray', 'tab:cyan', 'tab:purple', 'tab:pink', 'tab:brown']

plt.bar(tickers, percentage_change, label=bar_labels, color=bar_colors)
plt.bar_label(bars, labels = percentage_change, label_type = 'center')
plt.ylabel('Percentage Change')
plt.title('Percentage Change in Stock Prices')
#ax.legend(title='Stocks and Percentage Change')

plt.show()
