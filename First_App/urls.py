from django.urls import path
from First_App.views import *

urlpatterns = [
    path('', index_view),
    path('about', about_view),
    path('contact', contact_view)
    
]