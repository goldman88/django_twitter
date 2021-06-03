# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
#import tweepy
from tweepy import API 
from tweepy import OAuthHandler
import numpy as np
import pandas as pd

# The consumer key and secret will be generated for you after
consumer_key="EMuIyUFtxiEo5RfpPK9CD69o9"
consumer_secret="drX2XM0uZc0cdtwlaAUn3yk3dLv8e1jvv7qDCbIieCZJDiOuFJ"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="1293664654884048896-zJCE4qlGw8RwUXQBva2AxOKxvkDMak"
access_token_secret="NudYPd8KZQWaK4QfNW6FDgKNnClOpkdlCsS6x6fdA4Kij"

@login_required(login_url="/login/")
def index(request):
    
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

#Clean Twitter data using Pandas DataFrame
def tweets_to_data_frame(tweets):
    df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
    df['id'] = np.array([tweet.id for tweet in tweets])
    df['len'] = np.array([len(tweet.text) for tweet in tweets])
    df['date'] = np.array([tweet.created_at for tweet in tweets])
    df['source'] = np.array([tweet.source for tweet in tweets])
    df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
    df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
    df['geo'] = np.array([tweet.geo for tweet in tweets])
    
    return df

@login_required(login_url="/login/")
def pages(request):
    context = {}

    handle = "SkyCirclesLA"
    amount = 60
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = API(auth,wait_on_rate_limit=True)
    tweets = api.user_timeline(screen_name=handle, count=amount)
    df = tweets_to_data_frame(tweets)

    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        context['data'] = df
        context['handle'] = handle
        context['count'] = amount
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))
