from constants import WEATHER_URL, CURRENCY_URL, DEFAULTS, CURRENCIES, RSS_FEEDS, WEATHER_URL_TOKEN
from flask import Flask, render_template, request, make_response
import feedparser
import urllib
import json
import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    publication = getPublicationQuery(request)
    articles = getNews(publication)

    city = getCityQuery(request)
    weather = getWeather(city)

    currencyFrom = getCurrencyFromQuery(request)
    currencyTo = getCurrencyToQuery(request)
    rateData = getRate(currencyFrom, currencyTo)

    if not rateData["currencies"]:
        rateData["currencies"] = CURRENCIES
    response = make_response(render_template("home.html", 
                           articles=articles, 
                           weather=weather, 
                           rateData=rateData,
                           publications=RSS_FEEDS.keys(),
                           publication=publication
                        ))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_to", currencyTo, expires=expires)
    response.set_cookie("currency_from", currencyFrom, expires=expires)
    return response

def getRate(frm, to):
    if "select" in frm:
        frm = DEFAULTS["currency_from"]
    
    if "select" in to:
        to = DEFAULTS["currency_to"]
    
    all_currency = urllib.request.urlopen(CURRENCY_URL).read()
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return {
        "rate": to_rate/frm_rate, 
        "from": frm.upper(), 
        "to": to.upper(), 
        "currencies": sorted(parsed.keys())
        }

def getQuery(req, key="publication"):
    query = None
    if req.method == "POST" and key in req.form:
        query = req.form[key]

    if req.method == "GET" and key in req.args:
        query = req.args.get(key)

    if not query:
        query = req.cookies.get(key)

    if not query:
        query = DEFAULTS[key]
    print(key, query)
    return query.lower()

def getPublicationQuery(req):
    return getQuery(req)

def getNews(publication):
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed["entries"]

def getCityQuery(req):
    return getQuery(req, "city")

def getCurrencyFromQuery(req):
    return getQuery(req, "currency_from")

def getCurrencyToQuery(req):
    return getQuery(req, "currency_to")

def getWeather(query):
    query = urllib.parse.quote(query)
    url = WEATHER_URL.format(query, WEATHER_URL_TOKEN)
    data = urllib.request.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {
            "description": parsed["weather"][0]["description"], 
            "temperature": parsed["main"]["temp"], 
            "city": parsed["name"],
            'country': parsed['sys']['country']
        }
    return weather

if __name__ == "__main__":
    app.run(port=5000, debug=True)