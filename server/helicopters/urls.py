from django.conf.urls import url, include
from django.contrib import admin

from landing.views import home_page, login_page, signup_page, manager_page

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home_page, name='home_page'),
    url(r'^login/$', login_page, name='login_page'),
    url(r'^signup/$', signup_page, name='signup_page'),
    url(r'^manager/$', manager_page, name='manager_page'),

    url(r'^api/v1/', include('helipads.urls')),
    url(r'^api/v1/', include('landing.urls')),
]
