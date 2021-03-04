"""
    The app's route handler.

    Handles requests an redirect them to an appropriate view.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('about', views.about, name='about'),
    path('compute', views.compute, name='compute'),
    path('imprint', views.imprint, name='imprint'),
    path('methods', views.methods, name='methods'),
    path('privacy', views.privacy, name='privacy'),
    path('results_nv', views.results_nv, name='results_nv'),
    path('results_gv', views.results_gv, name='results_gv'),
    path('results_bv', views.results_bv, name='results_bv'),
    path('welcome', views.welcome, name='welcome')
]
