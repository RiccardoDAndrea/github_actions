import smtplib, ssl
import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
from matplotlib import pyplot as plt


tickers = ['AAPL', 'BYDDF', 'EONGY', 'LNVGF', 'NIO', 'PLUN.F', 'TSLA', 'TKA.DE', 'XIACF']
end_date = datetime.today()
start_date = end_date - timedelta(days= 2 * 365)

close_df = pd.DataFrame()


# close_df.reset_index(inplace=True)
df = pd.read_csv('close_data.csv')

#### P E R S O N A L _ S T O C K S ####

tickers = ['AAPL', 'BYDDF', 'EONGY', 'LNVGF', 'NIO', 'PLUN.F', 'TSLA', 'TKA.DE', 'XIACF']
stock_buy_price = [110.96, 24.95, 11.47, 1.419, 47.81, 45.544, 159.95, 6.799474, 1.6198]

#### C A L C I L A T E _ P E R C E N T A G E _ C H A N G E

stock_close_price = df.iloc[-1, 1:].tolist()
percentage_change = [(close_price - buy_price) / buy_price * 100 for close_price, buy_price in zip(stock_close_price, stock_buy_price)]
percentage_change = [round(change, 2) for change in percentage_change]


#### V I S U A L I Z A T I O N _ O F _ S T O C K S
plt.figure(figsize = (10,6))
bars = plt.bar(tickers, percentage_change, color = 'tab:blue')


bar_labels = [f"{ticker} ({change:.2f}%)" for ticker, change in zip(tickers, percentage_change)]
bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:gray', 'tab:cyan', 'tab:purple', 'tab:pink', 'tab:brown']

plt.bar(tickers, percentage_change, label=bar_labels, color=bar_colors)
plt.bar_label(bars, labels = percentage_change, label_type = 'center')
plt.ylabel('Percentage Change')
plt.title('Percentage Change in Stock Prices')
#ax.legend(title='Stocks and Percentage Change')

# S A V E _ A S _ I M A G E
image_file_name = 'stock_prices.png'
plt.savefig(image_file_name)
plt.show()