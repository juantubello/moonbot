# -*- coding: utf-8 -*-

import tweepy
import os
import time
import json
import requests
import datetime
import pytz

# Lunar phases emojis
LUNA_NUEVA     = '\U0001F311'
LUNA_CRECIENTE = '\U0001F312'
LUNA_MENGUANTE = '\U0001F318'
LUNA_LLENA     = '\U0001F315'

# Creds to use Tweepy API
CONSUMER_KEY    = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_KEY      = os.getenv('ACCESS_KEY')
ACCESS_SECRET   = os.getenv('ACCESS_SECRET')

#End Point
API_ENDPOINT    = os.getenv('API_ENDPOINT')

def auth_in_tweepy(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET):
    """
    Take twitter keys as string to log into @MoonBotVL using tweepy library
    """
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    return api

def tweet(tweet_to_tweet, moon_bot_acc):
    """
    Take a string and a tweepy logged instance, to tweet.
    """
    try:
        if moon_bot_acc.update_status(status=tweet_to_tweet):
            print("Tweeted OK")
    except tweepy.error.TweepError as e:
        print(e)

## Logic ##

INTERVAL = 24 * 60 * 60  # Day Interval

api = auth_in_tweepy(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)

while True:

 # Consuming meteored api filtering - Argentina/Buenos Aires/ Vicente Lopez
 response = requests.get(API_ENDPOINT)
 data = response.json()

 day_of_week = data["day"]["1"]["name"]
 date = data["day"]["1"]["date"]
 moon_desc = data["day"]["1"]["moon"]["desc"]
 moon_out = data["day"]["1"]["sun"]["out"]

 # Setting the emoji of lunar phase according to api's moon description
 if 'Menguante' in moon_desc:
    emoji = LUNA_MENGUANTE

 elif 'Nueva' in moon_desc:
    emoji = LUNA_NUEVA

 elif 'Llena' in moon_desc:
    emoji = LUNA_LLENA

 elif 'Creciente' in moon_desc:
    emoji = LUNA_CRECIENTE

 # Argentina's datetime
 arg_tz = pytz.timezone("America/Argentina/Buenos_Aires")
 arg_info = datetime.datetime.now(arg_tz)
 arg_date = arg_info.strftime("%Y-%m-%d")
 arg_date = arg_date.replace('-', '')

 if (date == arg_date):
     print("Date OK")
     moon_description = "Hoy " + day_of_week + " vamos a tener una... " + emoji + \
         " " + moon_desc + "!" + " → Su salida seria a las " + moon_out + " PM"
     tweet(moon_description, api)

 time.sleep(INTERVAL)
