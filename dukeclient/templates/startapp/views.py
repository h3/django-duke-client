# -*- coding: utf-8 -*-

from django.views.generic import ListView, TemplateView, DetailView
from %(project_name)s.models import *


class HomeView(TemplateView):
    template_name = '%(project_name)s/home.html'
