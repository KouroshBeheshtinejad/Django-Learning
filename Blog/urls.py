from django.urls import path
from Blog.views import *

app_name = 'Blog'

urlpatterns = [
    path('', blog_view,name='index'),
    path('<int:pid>', blog_single,name='single'),
    path('category/<str:cat_name>', blog_view,name='category'),
    path('test', test,name='test'),
]