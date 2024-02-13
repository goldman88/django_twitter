# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.utils.timezone import make_aware
from tweepy import API
from tweepy import OAuthHandler
import numpy as np
import pandas as pd

from .models import Tweet

# The consumer key and secret will be generated for you after
consumer_key = "EMuIyUFtxiEo5RfpPK9CD69o9"
consumer_secret = "drX2XM0uZc0cdtwlaAUn3yk3dLv8e1jvv7qDCbIieCZJDiOuFJ"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token = "1293664654884048896-zJCE4qlGw8RwUXQBva2AxOKxvkDMak"
access_token_secret = "NudYPd8KZQWaK4QfNW6FDgKNnClOpkdlCsS6x6fdA4Kij"


@login_required(login_url="/login/")
def index(request):

    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))

# Clean Twitter data using Pandas DataFrame


def tweets_to_data_frame(tweets):
    df = pd.DataFrame(
        data=[tweet.text for tweet in tweets], columns=['Tweets'])
    df['id'] = np.array([tweet.id for tweet in tweets])
    df['len'] = np.array([len(tweet.text) for tweet in tweets])
    df['date'] = np.array([tweet.created_at for tweet in tweets])
    df['source'] = np.array([tweet.source for tweet in tweets])
    df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
    df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
    df['geo'] = np.array([tweet.geo for tweet in tweets])

    return df

# Note: This version does not use HttpResponseRedirect as the form data uses 'GET' does not modify the database


@login_required(login_url="/login/")
def tweethistory(request):
    context = {}
    context['segment'] = "ui-twitter-tables"
    context['count'] = 250
    # load blank page...i.e no post data...empty context/error message
    try:
        context['twitter_handle'] = request.GET['twitter_handle']
    except (KeyError):
        context['error_message'] = "No twitter handle entered"
        return render(request, 'ui-twitter-tables.html', context)
    else:
        # TODO - remember to deal with the error if twitter handle is incorrect
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = API(auth, wait_on_rate_limit=True)
        tweets = api.user_timeline(
            screen_name=context['twitter_handle'], count=context['count'])
        df = tweets_to_data_frame(tweets)
        context['data'] = df

        # Populate database
        # Iterate through all the rows in the data frame
        for index, row in df.iterrows():

            # Make date timezone aware
            naive_datetime = row['date']
            aware_datetime = make_aware(naive_datetime)

            # First verify that the tweet (using the tweet id from twitter does not already exist before adding to database)
            # Alternative: Can use Tweet.objects.get_or_create to avoid the boilerplate code below
            #https://docs.djangoproject.com/en/3.2/ref/models/querysets/#get-or-create
            # obj, created = Tweet.objects.get_or_create(tweet_id=row['id'],defaults={
            #    'tweet_handle': context['twitter_handle'],
            #    'tweet_date': row['date'],
            #    'tweet_location': row['geo']
            # })

            # Process location data; separate into x and y
            if type(row['geo']) is dict:
                x_coord = row['geo']['coordinates'][0]
                y_coord = row['geo']['coordinates'][1]
            else:
                x_coord = 0.0
                y_coord = 0.0

            try:  # Check if the tweet already exist in the database
                obj = Tweet.objects.get(tweet_id=row['id'])
            except Tweet.DoesNotExist:  # If not, insert the specific columns into the database
                Tweet.objects.create(
                    tweet_handle=context['twitter_handle'],
                    tweet_id=row['id'],
                    tweet_date=aware_datetime,
                    tweet_location_x=x_coord,
                    tweet_location_y=y_coord)

            # Note: instead of passing data directly to context from tweepy, can read from database but it will be more expensive i.e. a noteable
            # performance hit

        return render(request, 'ui-twitter-tables.html', context)


@login_required(login_url="/login/")
def pages(request):
    context = {}

    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))
