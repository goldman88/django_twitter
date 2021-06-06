# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path

#change to: from . import views
from . import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    #view that is used if no user handle is provided
    path('tweethistory/', views.tweethistory, name='tweethistory'),

    # View that is used if user handle is provided in URL
    #path('tweethistory/<str:handle>/', views.tweethistory, name='tweethistory'),

    # Matches any html file
    # FIXME: this URL pattern cause an error if a trailing '/' is not included for pattern 'tweethistory'
    re_path(r'^.*\.*', views.pages, name='pages'),

]