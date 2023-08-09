import smtplib
import ssl
import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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

#### P E R S O N A L _ S T O C K S ####

tickers = ['AAPL', 'BYDDF', 'EONGY', 'LNVGF', 'NIO', 'PLUN.F', 'TSLA', 'TKA.DE', 'XIACF']
stock_buy_price = [110.96, 24.95, 11.47, 1.419, 47.81, 45.544, 159.95, 6.799474, 1.6198]
quantitiy_of_stocks = [1, 9, 11.3111, 10, 10, 5, 3, 19, 10]

#### C A L C I L A T E _ P E R C E N T A G E _ C H A N G E

stock_close_price = close_df.iloc[-1, 1:].tolist()
percentage_change = [(close_price - buy_price) / buy_price * 100 for close_price, buy_price in zip(stock_close_price, stock_buy_price)]
percentage_change = [round(change, 2) for change in percentage_change]

sum_of_stocks = [price * quantity for price, quantity in zip(stock_close_price, quantitiy_of_stocks)]

#### V I S U A L I Z A T I O N _ O F _ S T O C K S
plt.figure(figsize = (10,6))
bars = plt.bar(tickers, percentage_change, color = 'tab:blue')


bar_labels = [f"{ticker} ({change:.2f}%)" for ticker, change in zip(tickers, percentage_change)]
bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:gray', 'tab:cyan', 'tab:purple', 'tab:pink', 'tab:brown']

plt.bar(tickers, percentage_change, label=bar_labels, color=bar_colors)
plt.bar_label(bars, labels = percentage_change, label_type = 'center')
plt.ylabel('Percentage Change')
plt.title('Percentage Change in Stock Prices over the last 2 years')
#ax.legend(title='Stocks and Percentage Change')

# S A V E _ A S _ I M A G E
image_file_name = 'stock_prices.png'
plt.savefig(image_file_name)

plt.figure(figsize=(18,10))
plt.title('Share risk distribution')
plt.pie(sum_of_stocks, labels=tickers)

pie_image_file_name = 'share_risk_distribution.png'
plt.savefig(pie_image_file_name)
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
body = "Das ist eine automatisierte Mail mit einem Graphen der Schlusskurse der ausgewählten Aktien im Anhang."
message.attach(MIMEText(body, 'plain'))

# A T T C H M E N T 

with open(image_file_name, 'rb') as attachment:
    part = MIMEText(attachment.read(), 'png', _charset='utf-8')
    part.add_header('Content-Disposition', 'attachment', filename=image_file_name)
    message.attach(part)

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(USERNAME, PASSWORD)
    server.sendmail(USERNAME, USERNAME, message.as_string())

