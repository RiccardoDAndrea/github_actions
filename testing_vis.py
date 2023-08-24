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
last_week_data = df.tail(7)

# Daten der letzten Woche vorbereiten
last_week_data['Date'] = pd.to_datetime(last_week_data['Date'])  # Konvertieren in Datetime-Objekte
last_week_dates = last_week_data['Date'].dt.strftime('%Y-%m-%d')  # Datum formatieren
percentage_changes = (last_week_data.iloc[:, 1:-1] / last_week_data.iloc[:, 1:-1].shift(1) - 1) * 100    

bar_labels = [f"{ticker} ({change:.2f}%)" for ticker, change in zip(tickers, percentage_change)]
bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:gray', 'tab:cyan', 'tab:purple', 'tab:pink', 'tab:brown']

#### V I S U A L I Z A T I O N _ O F _ S T O C K S
plt.style.use('seaborn')
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 9))
fig.suptitle('Stock performance Overview', fontsize=16, y=0.98, x=0.29)
plt.subplots_adjust(wspace=0.3, hspace=0.6)  # Horizontale und vertikale Abstände anpassen

#plt.style.use('seaborn-colorblind')
# F I R S T _ C H A R T -> Säulen Diagram

ax1.plot(last_week_dates, percentage_changes, marker='o')
ax1.set_xticks(last_week_dates)  # X-Ticks setzen
ax1.set_xticklabels(last_week_dates, rotation=45)
ax1.set_xlabel('Date')
ax1.set_ylabel('Percentage Change')
ax1.set_title('Stock Price Performance Last Week')
# S E C O N D _ P L O T -> Linen Diagramm

# Daten in aufsteigender Reihenfolge sortieren (größte positive Änderung oben)
sorted_indices = sorted(range(len(percentage_change)), key=lambda k: percentage_change[k])
sorted_tickers = [tickers[i] for i in sorted_indices]
sorted_percentage_change = [percentage_change[i] for i in sorted_indices]
sorted_bar_labels = [bar_labels[i] for i in sorted_indices]

# Balkendiagramm erstellen
bars = ax2.barh(sorted_tickers, sorted_percentage_change, color=bar_colors)
ax2.bar_label(bars, labels=sorted_bar_labels, label_type='center')
ax2.set_xlabel('Percentage Change')
# X-Achsenbeschriftungen entfernen
ax2.set_xticklabels([], rotation=45)
ax2.set_title('Percentage Change over the last two years')

# T H I R D _ P L O T -> Linen Diagramm
ax3.set_title('Share risk distribution')
ax3.pie(sum_of_stocks, labels=tickers)

# F O U R T H _ P L O T -> Linen Diagramm

for ticker in tickers:
    ax4.plot(df['Month_Year'], df[ticker], label=ticker)
ax4.set_xticklabels(df['Month_Year'].dt.strftime('%Y-%m') , rotation=45)
ax4.set_xlabel('Month_Year')
ax4.set_ylabel('Stock Price')
ax4.set_title('Stock Prices Over the last two years')
plt.legend(loc='best', mode='expand',ncol=3, bbox_to_anchor=(0,1,1,2), fontsize='small')




#### S E C O N D _ P L O T _ C R E A T I O N _ O F _ P I E _ C H A R T -> Kuchen Diagramm 

plt.figure(figsize=(5,8))
plt.pie(sum_of_stocks, labels=tickers)
plt.tight_layout()
pie_image_file_name = 'share_risk_distribution.png'
plt.savefig(pie_image_file_name)

# S A V E _ A S _ I M A G E

image_file_name = 'stock_prices.png'
plt.savefig(image_file_name)
plt.show()
