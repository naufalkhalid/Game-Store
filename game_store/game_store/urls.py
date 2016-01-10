"""game_store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', views.home, name='index'),

    url(r'^signin$', views.sign_in, name='signin'),
    url(r'^signup$', views.sign_up, name='signup'),
    url(r'^signout$', views.sign_out, name='signout'),

    url(r'^game/(\d+)$', views.game, name='game'),

    url(r'^ajax/score$', views.score, name='score'),
    url(r'^ajax/state$', views.state, name='state'),

    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^add_game$', views.add_game, name='add_game'),
]
