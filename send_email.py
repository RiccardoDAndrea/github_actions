import smtplib
import ssl
import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from matplotlib import pyplot as plt
from io import BytesIO
import markdown2
#### G E T _ S T O C K _ P R I C E S ####

tickers = ['AAPL', 'BYDDF', 'EONGY', 'LNVGF', 'NIO', 'PLUN.F', 'TSLA', 'TKA.DE', 'XIACF']
end_date = datetime.today()
start_date = end_date - timedelta(days= 2 * 365)

close_df = pd.DataFrame()

for ticker in tickers:
    data = yf.download(ticker, start = start_date, end = end_date)
    close_df[ticker] = data['Close']
 
close_df.reset_index(inplace=True)
close_df['Date'] = pd.to_datetime(close_df['Date'])
close_df['Month_Year'] = close_df['Date'].dt.to_period('M')
close_df['Month_Year'] = close_df['Month_Year'].dt.to_timestamp()
print(close_df.tail())
#### P E R S O N A L _ S T O C K S ####

tickers = ['AAPL', 'BYDDF', 'EONGY', 'LNVGF', 'NIO', 'PLUN.F', 'TSLA', 'TKA.DE', 'XIACF']
stock_buy_price = [110.96, 24.95, 11.47, 1.419, 47.81, 45.544, 159.95, 6.799474, 1.6198]
quantitiy_of_stocks = [1, 9, 11.3111, 10, 10, 5, 3, 19, 10]

#### C A L C I L A T E _ P E R C E N T A G E _ C H A N G E

stock_close_price = close_df.iloc[-1, 1:].tolist()
percentage_change = [(close_price - buy_price) / buy_price * 100 for close_price, buy_price in zip(stock_close_price, stock_buy_price)]
percentage_change = [round(change, 2) for change in percentage_change]

sum_of_stocks = [price * quantity for price, quantity in zip(stock_close_price, quantitiy_of_stocks)]
last_week_data = close_df.tail(7)


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

# F I R S T _ C H A R T -> Säulen Diagram
ax1.plot(last_week_dates, percentage_changes, marker='o')
ax1.set_xticks(last_week_dates)  # X-Ticks setzen
ax1.set_xticklabels(last_week_dates, rotation=45)
ax1.set_xlabel('Date')
ax1.set_ylabel('Percentage Change')
ax1.set_title('Stock Price Performance Last Week')
# S E C O N D _ P L O T -> Linen Diagramm

# Daten der letzten Woche vorbereiten
last_week_data['Date'] = pd.to_datetime(last_week_data['Date'])  # Konvertieren in Datetime-Objekte
last_week_dates = last_week_data['Date'].dt.strftime('%Y-%m-%d')  # Datum formatieren
percentage_changes = (last_week_data.iloc[:, 1:-1] / last_week_data.iloc[:, 1:-1].shift(1) - 1) * 100
sum_of_stocks = [price * quantity for price, quantity in zip(stock_close_price, quantitiy_of_stocks)]

# Prozentuale Veränderung der Aktienkurse über die letzte Woche plotten (Liniendiagramm)
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
    ax4.plot(close_df['Month_Year'], close_df[ticker], label=ticker)
ax4.set_xticklabels(close_df['Month_Year'].dt.strftime('%Y-%m') , rotation=45)
ax4.set_xlabel('Month_Year')
ax4.set_ylabel('Stock Price')
ax4.set_title('Stock Prices Over the last two years')
plt.legend(loc='best', mode='expand',ncol=3, bbox_to_anchor=(0,1,1,2), fontsize='small')




#### S E C O N D _ P L O T _ C R E A T I O N _ O F _ P I E _ C H A R T -> Kuchen Diagramm 

plt.figure(figsize=(5,8))
plt.pie(sum_of_stocks, labels=tickers)
plt.tight_layout()
pie_image_file_name = 'share_risk_distribution.png'
fig.savefig(pie_image_file_name)

# S A V E _ A S _ I M A G E

image_file_name = 'stock_prices.png'
plt.savefig(image_file_name)
plt.close()


#### S E N D I N G _ E - M A I L ####

port = 465
smtp_server = "smtp.gmail.com"
USERNAME = os.environ.get('USER_EMAIL')
PASSWORD = os.environ.get('USER_PASSWORD')

# C R E A T E _ M A I L 

message = MIMEMultipart()
message['From'] = USERNAME
message['To'] = USERNAME
message['Subject'] = "GitHub Email Report"
# DataFrame als HTML-Tabelle mit Gitterlinien formatieren
html_table = close_df.tail().to_html(index=False, classes='table', border=1)

# Generieren des formatierten Texts mit Sternchen für Fettdruck
last_closing_prices = close_df.tail().round(2)

body = f"""
Good day users,

Here is your weekly report on your stocks.

Your stock portfolio consists of the following stocks: 
{', '.join(tickers)}

They were bought at the following prices:
{', '.join([f'{ticker}: ${price:.2f}' for ticker, price in zip(tickers, stock_buy_price)])}

The last closing prices were as follows:

{last_closing_prices.to_string(index=False, line_width=100, justify='center')}
"""



message.attach(MIMEText(body, 'plain'))
# A T T C H M E N T 

with open(image_file_name, 'rb') as attachment_line_chart:
    part_1 = MIMEImage(attachment_line_chart.read(), name=image_file_name)
    part_1.add_header('Content-Disposition', 'attachment', filename=image_file_name)
    message.attach(part_1)

# Attach the second image (pie chart)
with open(pie_image_file_name, 'rb') as attachment_pie_chart:
    part_2 = MIMEImage(attachment_pie_chart.read(), name=pie_image_file_name)
    part_2.add_header('Content-Disposition', 'attachment', filename=pie_image_file_name)
    message.attach(part_2)

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(USERNAME, PASSWORD)
    server.sendmail(USERNAME, USERNAME, message.as_string())
