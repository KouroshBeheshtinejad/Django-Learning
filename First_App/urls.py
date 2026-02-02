from django.urls import path
from First_App.views import http_test, json_test

urlpatterns = [
    path('http-test', http_test),
    path('json-test', json_test)
]