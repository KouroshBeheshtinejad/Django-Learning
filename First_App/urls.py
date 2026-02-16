from django.urls import path
from First_App.views import *

app_name = 'First_App'

urlpatterns = [
    path('', index_view,name='index'),
    path('about', about_view,name='about'),
    path('contact', contact_view,name='contact'),
    path('elements', elements_view,name='elements'),
    path('test', test_view,name='test'),
    path('newsletter', newsletter_view,name='newsletter'),
]