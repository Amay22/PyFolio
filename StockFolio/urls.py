'''Urls for the StockFolio app'''
from django.conf.urls import url
from . import views as StockFolio_views

urlpatterns = [
    url(r'^(?i)portfolio', StockFolio_views.portfolio, name="portfolio")
]
