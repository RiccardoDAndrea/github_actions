import smtplib, ssl
import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from matplotlib import pyplot as plt
from io import BytesIO

# #### G E T _ S T O C K _ P R I C E S ####

# tickers = ['AAPL', 'BYDDF', 'EONGY', 'LNVGF', 'NIO', 'PLUN.F', 'TSLA', 'TKA.DE', 'XIACF']
# end_date = datetime.today()
# start_date = end_date - timedelta(days=2 * 365)

# close_df = pd.DataFrame()

# for ticker in tickers:
#     data = yf.download(ticker, start=start_date, end=end_date)
#     close_df[ticker] = data['Close']

# close_df.reset_index(inplace=True)

# #### P L O T ####

# plt.figure(figsize=(10, 6))
# for ticker in tickers:
#     plt.plot(close_df['Date'], close_df[ticker], label=ticker)
# plt.legend()
# plt.xlabel('Date')
# plt.ylabel('Close Price')
# plt.title('Close Prices of Selected Stocks')

# # Speichern des Graphen als Bild
# image_file_name = 'stock_prices.png'
# plt.savefig(image_file_name)
# plt.close()

#### S E N D I N G _ E - M A I L ####
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

#### P L O T ####

tickers = ['AAPL', 'BYDDF', 'EONGY', 'LNVGF', 'NIO', 'PLUN.F', 'TSLA', 'TKA.DE', 'XIACF']
stock_buy_price = [110.96, 24.95, 11.47, 1.419, 47.81, 45.544, 159.95, 6.799474, 1.6198]

# Calculate percentage change
stock_close_price = data.iloc[-1, 1:].tolist()
percentage_change = [(close_price - buy_price) / buy_price * 100 for close_price, buy_price in zip(stock_close_price, stock_buy_price)]
percentage_change = [round(change, 2) for change in percentage_change]


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

# Speichern des Graphen als Bild
image_file_name = 'stock_prices.png'
plt.savefig(image_file_name)
plt.close()

#### S E N D I N G _ E - M A I L ####

port = 465
smtp_server = "smtp.gmail.com"
USERNAME = os.environ.get('USER_EMAIL')
PASSWORD = os.environ.get('USER_PASSWORD')

# Erstelle die E-Mail
message = MIMEMultipart()
message['From'] = USERNAME
message['To'] = USERNAME
message['Subject'] = "GitHub Email Report"
body = "Das ist eine automatisierte Mail mit einem Graphen der Schlusskurse der ausgewählten Aktien im Anhang."
message.attach(MIMEText(body, 'plain'))

# Füge den Graphen als Anhang hinzu
with open(image_file_name, 'rb') as attachment:
    part = MIMEText(attachment.read(), 'png', _charset='utf-8')
    part.add_header('Content-Disposition', 'attachment', filename=image_file_name)
    message.attach(part)

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(USERNAME, PASSWORD)
    server.sendmail(USERNAME, USERNAME, message.as_string())

