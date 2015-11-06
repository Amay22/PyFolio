'''Urls for the LoginFolio app'''
from django.conf.urls import url
from . import views as LoginFolio_views

urlpatterns = [
    url(r'^(?i)login', LoginFolio_views.login_user, name="login"),
    url(r'^(?i)logout', LoginFolio_views.logout_user, name="logout"),
    url(r'^(?i)register', LoginFolio_views.register_user, name="register"),
]
