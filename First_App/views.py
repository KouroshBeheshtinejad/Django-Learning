from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from Blog.models import Post
from First_App.models import Contact, Newsletter  
from First_App.forms import ContactForm, NewsletterForm
from django.contrib import messages


def index_view(request):
    latest_posts = Post.objects.filter(status=1).order_by('-published_date')[:6]
    context = {'latest_posts': latest_posts}
    return render(request, 'website/index.html', context)


def about_view(request):
    return render(request, 'website/about.html')


def contact_view(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data['name'] = 'ناشناس'
        form = ContactForm(post_data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
        else:
            messages.error(request, 'There was an error sending your message. Please try again.')
    form = ContactForm()
    context = {'form': form}
    return render(request, 'website/contact.html', context)


def newsletter_view(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')


def test_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Form submitted successfully!')
        elif form.errors:
            return HttpResponse(f'Form errors: {form.errors}')
    form = ContactForm()
    context = {'form': form}
    return render(request, 'test.html', context)