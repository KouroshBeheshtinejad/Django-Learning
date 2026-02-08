from django.urls import path
from Blog.views import *

app_name = 'Blog'

urlpatterns = [
    path('', blog_view,name='index'),
    path('single', blog_single,name='single'),
]