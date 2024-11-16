from django.conf.urls import handler404
from django.urls import path
from .views import *


handler404 = err404

urlpatterns = [
    path("",index,name="intro"),
    path("signup/",signup,name="signup"),
    path("setup/",accountsetup,name="setup"),
    path("login/",loginUser,name="loginUser"),
    path("home/",home,name="home"),
    path("login/",logoutUser,name="logoutUser"),
    path("anime/",anime,name="anime"),
    path("community-forum/",community,name="community"),
    path('manage/',operations,name="operations"),
    path('storage/',storage,name="storage"),
    path('analytics/',analytics,name="analytics"),
    path("anime/<slug:title>/",seasons,name="seasons"),
    path("anime/<slug:title>/season-<int:seasons>/",episodes,name="episodes"),
    # path("404/",)
    
]
