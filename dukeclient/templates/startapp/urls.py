# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
#from django.conf import settings
from %(project_name)s.views import *

urlpatterns=patterns('',
    url(r'^$',          HomeView.as_view(),     name='%(project_name)s-home'),
)
