from tokens import WEATHER_URL_TOKEN, CURRENCY_URL_TOKEN

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(WEATHER_URL_TOKEN)

CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id={}".format(CURRENCY_URL_TOKEN)

RSS_FEEDS = {
    'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn': 'http://rss.cnn.com/rss/edition.rss',
    'fox': 'http://feeds.foxnews.com/foxnews/latest',
    'iol': 'http://www.iol.co.za/cmlink/1.640'
}

DEFAULTS = {
    "publication": "bbc", 
    "city": "Accra,GH",
    'currency_from':'GBP',
    'currency_to':'USD'
}

CURRENCIES = {
    "USD",
    "GBP",
    "EUR",
    "ZAR",
}