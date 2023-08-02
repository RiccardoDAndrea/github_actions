import smtplib, ssl
import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# port = 465
# smtp_server = "smtp.gmail.com"
# USERNAME = os.environ.get('USER_EMAIL')
# PASSWORD = os.environ.get('USER_PASSWORD')
# message = """\
# Subject: GitHub Email Report
# Das ist eine Automatisierte Mail
# """

# context = ssl.create_default_context()
# with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
#     server.login(USERNAME,PASSWORD)
#     server.sendmail(USERNAME,USERNAME,message)

#### E N D _ S E N D I N G _ E - M A I L ####

#### G E T _ S T O C K _ P R I C E S ####

tickers = ['AAPL', 'BYDDF']

end_date = datetime.today()

start_date = end_date - timedelta(days = 2 * 365)

close_df = pd.DataFrame()

for ticker in tickers:
    data = yf.download(ticker,start=start_date, end=end_date)
    close_df[ticker] = data['Close']

print(close_df)