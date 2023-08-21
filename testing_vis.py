import smtplib, ssl
import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.dates import date2num, DateFormatter
from pandas.plotting import table


end_date = datetime.today()
start_date = end_date - timedelta(days= 2 * 365)

close_df = pd.DataFrame()

# close_df.reset_index(inplace=True)

df = pd.read_csv('close_data.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['Month_Year'] = df['Date'].dt.to_period('M')
df['Month_Year'] = df['Month_Year'].dt.to_timestamp()  # Konvertieren Sie die Period-Objekte in einen Zeitstempel.
#df['Month_Year'] = df['Month_Year'].apply(date2num) 

# change datatype to date
currentSecond= datetime.now().second
currentMinute = datetime.now().minute
currentHour = datetime.now().hour

currentDay = datetime.now().day
currentMonth = datetime.now().month
currentYear = datetime.now().year


#### P E R S O N A L _ S T O C K S ####

tickers = ['AAPL', 'BYDDF', 'EONGY', 'LNVGF', 'NIO', 'PLUN.F', 'TSLA', 'TKA.DE', 'XIACF']
stock_buy_price = [110.96, 24.95, 11.47, 1.419, 47.81, 45.544, 159.95, 6.799474, 1.6198]
quantitiy_of_stocks = [1, 9, 11.3111, 10, 10, 5, 3, 19, 10]

#### C A L C U L A T E _ P E R C E N T A G E _ C H A N G E

stock_close_price = df.iloc[-1, 1:].tolist()                                        # <- aktuelle schluss kurse der aktien ini tickers 
percentage_change = [(close_price - buy_price) / buy_price * 100 for close_price, buy_price in zip(stock_close_price, stock_buy_price)]  # dreissatz nur 
percentage_change = [round(change, 2) for change in percentage_change]              # runden auf 2 nach komma stellen

sum_of_stocks = [price * quantity for price, quantity in zip(stock_close_price, quantitiy_of_stocks)]
    
#### V I S U A L I Z A T I O N _ O F _ S T O C K S

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 12))
plt.subplots_adjust(wspace=0.3, hspace=0.6)  # Horizontale und vertikale Abstände anpassen

bars = ax2.barh(tickers, percentage_change, color = 'tab:blue')


bar_labels = [f"{ticker} ({change:.2f}%)" for ticker, change in zip(tickers, percentage_change)]
bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:gray', 'tab:cyan', 'tab:purple', 'tab:pink', 'tab:brown']

# F I R S T _ C H A R T -> Säulen Diagram
last_week_data = df.tail(7)

# Daten der letzten Woche vorbereiten
last_week_data['Date'] = pd.to_datetime(last_week_data['Date'])  # Konvertieren in Datetime-Objekte
last_week_dates = last_week_data['Date'].dt.strftime('%Y-%m-%d')  # Datum formatieren
percentage_changes = (last_week_data.iloc[:, 1:-1] / last_week_data.iloc[:, 1:-1].shift(1) - 1) * 100

# Prozentuale Veränderung der Aktienkurse über die letzte Woche plotten (Liniendiagramm)
ax1.plot(last_week_dates, percentage_changes, marker='o')
ax1.set_xticks(last_week_dates)  # X-Ticks setzen
ax1.set_xticklabels(last_week_dates, rotation=45)
ax1.set_xlabel('Date')
ax1.set_ylabel('Percentage Change')
ax1.set_title('Stock Price Performance Last Week')

# S E C O N D _ P L O T -> Linen Diagramm

bars = ax2.barh(tickers, percentage_change, color=bar_colors)
ax2.bar_label(bars, labels=bar_labels, label_type='center')
ax2.set_xlabel('Percentage Change')
# X-Achsenbeschriftungen entfernen
ax2.set_xticklabels([], rotation=45)
ax2.set_title('Percentage Change over the last two years')

# T H I R D _ P L O T -> Linen Diagramm




# F O U R T H _ P L O T -> Linen Diagramm

for ticker in tickers:
    ax4.plot(df['Month_Year'], df[ticker], label=ticker)
ax4.set_xticklabels(df['Month_Year'].dt.strftime('%Y-%m') , rotation=45)
ax4.set_xlabel('Month_Year')
ax4.set_ylabel('Stock Price')
ax4.set_title('Stock Prices Over the last two years')
# ax4.legend(title='Stocks and Percentage Change')


#### S E C O N D _ P L O T _ C R E A T I O N _ O F _ P I E _ C H A R T -> Kuchen Diagramm 

plt.figure(figsize=(5,8))
plt.title('Share risk distribution')
plt.pie(sum_of_stocks, labels=tickers)
plt.tight_layout()
# plt.legend(loc='upper left', bbox_to_anchor=(1, 1))  # Legende außerhalb des Diagramms platzieren
pie_image_file_name = 'share_risk_distribution.png'
plt.savefig(pie_image_file_name)

# S A V E _ A S _ I M A G E

image_file_name = 'stock_prices.png'
plt.savefig(image_file_name)
plt.show()
