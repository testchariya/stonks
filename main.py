import requests
# import datetime
from twilio.rest import Client

# today = datetime.datetime.today().date()
# yesterday = today - datetime.timedelta(days=1)
# daybefore = today - datetime.timedelta(days=2)

STOCK = "TSLA"
COMPANY_NAME = "Tesla"

## STEP 1: Use https://www.alphavantage.co GWZLRJJ9F8YEJOV8
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

av_param = {
    "function": 'TIME_SERIES_DAILY',
    "symbol": STOCK,
    "apikey": 'GWZLRJJ9F8YEJOV8',
}

url = 'https://www.alphavantage.co/query'
r = requests.get(url, params=av_param)
data = r.json()["Time Series (Daily)"]

data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
print(yesterday_data)
yesterday_closing_price = yesterday_data['4. close']
print(yesterday_closing_price)

day_before_data = data_list[1]
print(day_before_data)
day_before_closing_price = day_before_data['4. close']
print(day_before_closing_price)

perc_diff = (float(yesterday_closing_price) - float(day_before_closing_price)) / float(day_before_closing_price)
print(perc_diff)

text = str(round(perc_diff))

# daily_data = data["Time Series (Daily)"]
#
# today = list(daily_data.items())[0]
# today_date = today[0]
# today_close = today[1]["4. close"]
#
# yesterday = list(daily_data.items())[1]
# yesterday_date = yesterday[0]
# yesterday_close = yesterday[1]["4. close"]
#
# day_before = list(daily_data.items())[0]
# day_before_date = day_before[0]
# day_before_close = day_before[1]["4. close"]

# print(f"{today_date} close was {today_close}")
# today_pct_change = (float(today_close) - float(yesterday_close)) / float(yesterday_close)
# print(f"The change from previous day's close is {'{:.2%}'.format(today_pct_change)}")
# print(f"{yesterday_date} close was {yesterday_close}")

# yday_pct_change = (float(yesterday_close) - float(day_before_close)) / float(day_before_close)
# print(f"The change from previous day's close is {'{:.2%}'.format(yday_pct_change)}")
# print(f"{day_before_date} close was {day_before_close}")

# if abs(today_pct_change) > 0.05:
#     print("Gadzooks!")

# ydy_price = 1
# tdy_price = 1
# db4_price = 1

# for day in data["Time Series (Daily)"]:
#     if str(day) == str(today):
#         print(f"Today's ({day}) open:{daily_data[day]['1. open']} close:{daily_data[day]['4. close']}")
#         tdy_price = daily_data[day]['4. close']
#
#     if str(day) == str(yesterday):
#         print(f"Yesterday's ({day}) open:{daily_data[day]['1. open']} close:{daily_data[day]['4. close']}")
#         ydy_price = daily_data[day]['4. close']
#
#     if str(day) == str(daybefore):
#         print(f"Day before yesterday's ({day}) open:{daily_data[day]['1. open']} close:{daily_data[day]['4. close']}")
#         db4_price = daily_data[day]['4. close']

    # ydy_price = tdy_price
    # tdy_price = daily_data[day]['4. close']
    # pct_change = (float(tdy_price) - float(ydy_price))/float(ydy_price)
    # pct_change2 = (float(ydy_price) - float(db4_price))/float(db4_price)
    #
    # print(f"{'{:.2%}'.format(pct_change)} change {day} ended at {tdy_price} over yesterday's {ydy_price}")
    # print(f"{'{:.2%}'.format(pct_change2)} change {day-1} ended at {ydy_price} over day before's {db4_price}")

# print(f"The price deviation is {pct_change}")
#
# if abs(pct_change) >= 0.05:
#     print("The price deviation is over 5%")


## STEP 2: Use https://newsapi.org  be75f59f0c4b4dcc9a49088687c8ac5b
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
#
api_param = {
    "qInTitle": COMPANY_NAME,
    "apiKey": 'be75f59f0c4b4dcc9a49088687c8ac5b',
}

news_url = 'https://newsapi.org/v2/everything'
news_r = requests.get(news_url, params=api_param)
news_data = news_r.json()

# print(news_data)


article_1 = news_data['articles'][0]
article_2 = news_data['articles'][1]
article_3 = news_data['articles'][2]

text += f"Article #1: {article_1['title']}\n{article_1['content']}\n\n"
text += f"Article #2: {article_2['title']}\n{article_2['content']}\n\n"
text += f"Article #3: {article_3['title']}\n{article_3['content']}\n\n"

print(text)

## STEP 3: Use https://www.twilio.com
# Send a separate message with the percentage change and each article's title and description to your phone number.


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to
 file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height
  of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required
 to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the
  height of the coronavirus market crash.
"""

account_sid = 'AC6984f4bd665abb372a4f4687f93f163b'
auth_token = 'e3158bbbf6d5047f4a0605f9793b7291'

client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body=text,
                     from_='+16067220250',
                     to='+15627324462'
                 )

print(message.status)
