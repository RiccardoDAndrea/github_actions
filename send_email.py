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

#### P E R S O N A L _ S T O C K S ####

tickers = ['AAPL', 'BYDDF', 'EONGY', 'LNVGF', 'NIO', 'PLUN.F', 'TSLA', 'TKA.DE', 'XIACF']
stock_buy_price = [110.96, 24.95, 11.47, 1.419, 47.81, 45.544, 159.95, 6.799474, 1.6198]
quantitiy_of_stocks = [1, 9, 11.3111, 10, 10, 5, 3, 19, 10]
#### C A L C I L A T E _ P E R C E N T A G E _ C H A N G E

stock_close_price = close_df.iloc[-1, 1:].tolist()
percentage_change = [(close_price - buy_price) / buy_price * 100 for close_price, buy_price in zip(stock_close_price, stock_buy_price)]
percentage_change = [round(change, 2) for change in percentage_change]


#### V I S U A L I Z A T I O N _ O F _ S T O C K S
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 12))
plt.subplots_adjust(wspace=0.3, hspace=0.6)  # Horizontale und vertikale Abstände anpassen

bars = ax2.barh(tickers, percentage_change, color = 'tab:blue')


bar_labels = [f"{ticker} ({change:.2f}%)" for ticker, change in zip(tickers, percentage_change)]
bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:gray', 'tab:cyan', 'tab:purple', 'tab:pink', 'tab:brown']

# F I R S T _ C H A R T -> Säulen Diagram
last_week_data = close_df.tail(7)

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

bars = ax2.barh(tickers, percentage_change, color=bar_colors)
ax2.bar_label(bars, labels=bar_labels, label_type='center')
ax2.set_xlabel('Percentage Change')
# X-Achsenbeschriftungen entfernen
ax2.set_xticklabels([], rotation=45)
ax2.set_title('Percentage Change over the last two years')

# T H I R D _ P L O T -> Linen Diagramm




# F O U R T H _ P L O T -> Linen Diagramm

for ticker in tickers:
    ax4.plot(close_df['Month_Year'], close_df[ticker], label=ticker)
ax4.set_xticklabels(close_df['Month_Year'].dt.strftime('%Y-%m') , rotation=45)
ax4.set_xlabel('Month_Year')
ax4.set_ylabel('Stock Price')
ax4.set_title('Stock Prices Over the last two years')
# ax4.legend(title='Stocks and Percentage Change')

line_chart_image_file_name = 'line_chart_image_file_name.png'
plt.savefig(line_chart_image_file_name)
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
body = "Das ist eine automatisierte Mail mit einem Graphen der Schlusskurse der ausgewählten Aktien im Anhang."
message.attach(MIMEText(body, 'plain'))

# A T T C H M E N T 

with open(line_chart_image_file_name, 'rb') as attachment_line_chart:
    part_1 = MIMEImage(attachment_line_chart.read(), name=line_chart_image_file_name)
    part_1.add_header('Content-Disposition', 'attachment', filename=line_chart_image_file_name)
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
