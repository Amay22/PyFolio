'''Urls for the LoginFolio app'''
from django.conf.urls import url
from . import views as LoginFolio_views

urlpatterns = [
    url(r'^$', LoginFolio_views.login_user, name="login"),
    url(r'^(?i)login', LoginFolio_views.login_user, name="login"),
    url(r'^(?i)home', LoginFolio_views.home, name="home"),
    url(r'^(?i)about', LoginFolio_views.about, name="about"),
    url(r'^(?i)team', LoginFolio_views.team, name="team"),
    url(r'^(?i)logout', LoginFolio_views.logout_user, name="logout"),
    url(r'^(?i)register', LoginFolio_views.register_user, name="register")
]
