"""tp_laboratory_task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from filmApp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^film_card/.*', views.film_card_page, name='film_card'),
    url(r'^registration/.*', views.registration_page, name='registration'),
    url(r'^authorisation/.*', views.authorisation_page, name='authorisation'),
    url(r'^create_film_card/.*', views.create_edit_film, name='create_edit_film'),
    url(r'^main/.*$', views.main_page, name='main_page'),
    url(r'^profile/.*$', views.profile_page, name='profile'),
    url(r'^test/.*$', views.test, name='test'),
    url(r'^logout/.*$',views.user_logout, name='user_logout'),
    url(r'^api/film_list/.*$', views.api_film_list, name='api_film_list'),
    url(r'^api/film_card/.*$', views.api_film_card, name='api_film_card'),
    url(r'^appraisal/.*$', views.film_card_appraisal, name='appraisal'),
    url(r'^film_comment/.*$', views.film_comment, name='appraisal'),

]
