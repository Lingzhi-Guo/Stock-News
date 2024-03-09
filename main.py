import requests

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = "QQBOYSVKJ8GL7VQF"
NEWS_API_KEY = "64919a1a7c054e9cb3a10c8279ea95b8"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
ALERT_DIFFERENCE = 0.015

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}

stock_response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
stock_data = stock_response.json()
time_series = stock_data['Time Series (Daily)']
dates = list(time_series.keys())
yesterday_date = dates[0]
previous_date = dates[1]
yesterday_closing = float(time_series[yesterday_date]["4. close"])
previous_day_closing = float(time_series[previous_date]["4. close"])

news_parameters = {
    "q": COMPANY_NAME,
    "from": previous_date,
    "language": "en",
    "sortBy": "publishedAt",
    "apiKey": NEWS_API_KEY
}


if abs(yesterday_closing - previous_day_closing)/previous_day_closing >= ALERT_DIFFERENCE:
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    news_data = news_response.json()
    article = news_data["articles"][0]["title"]
    brief = news_data["articles"][0]["description"]
    link = news_data["articles"][0]["url"]
    if yesterday_closing > previous_day_closing:
        difference = (yesterday_closing - previous_day_closing)/previous_day_closing
        difference_percentage = "%.1f%%" % (difference * 100)
        print(f"TSLA: 🔺{difference_percentage}\nHeadline:👇\n{article}\nBrief:👇\n{brief}\nLink:👇\n{link}")
    else:
        difference = (previous_day_closing - yesterday_closing)/previous_day_closing
        difference_percentage = "%.1f%%" % (difference * 100)
        print(f"TSLA: 🔻{difference_percentage}\nHeadline:👇\n{article}\nBrief:👇\n{brief}\nLink:👇\n{link}")
else:
    print("Nothing remarkable.")


