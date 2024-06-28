from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^message/$', SendMail.as_view()),
    url(r'^email/$', SaveEmail.as_view()),
]
