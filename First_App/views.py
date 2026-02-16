from django.shortcuts import render
from Blog.models import Post

def index_view(request):
    latest_posts = Post.objects.filter(status=1).order_by('-published_date')[:6]
    context = {'latest_posts': latest_posts}
    return render(request, 'website/index.html', context)

def about_view(request):
    return render(request, 'website/about.html')

def contact_view(request):
    return render(request, 'website/contact.html')

def elements_view(request):
    return render(request, 'website/elements.html')