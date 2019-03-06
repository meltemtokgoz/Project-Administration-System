from django.conf.urls import url
from .views import *

app_name = 'account'

urlpatterns = [

    url(r'^login/$', login_view, name='login'),

    url(r'^newuser/$', user_view, name='newuser'),

    url(r'^logout/$', logout_view, name="logout"),

    url(r'^password/$', change_password, name='Change Password'),

]
