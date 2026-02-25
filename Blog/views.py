from django.shortcuts import render, get_object_or_404, redirect
from Blog.models import Post, Comment, PostView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Blog.forms import CommentForm
from django.contrib import messages


# Create your views here.
def blog_view(request, **kwargs):
    #--------- FILTERING ----------
    posts = Post.objects.filter(status=1)
    if kwargs.get('cat_name') != None :
        posts = posts.filter(category__name=kwargs['cat_name'])
    if kwargs.get('author_username') != None :
        posts = posts.filter(author__username=kwargs['author_username'])
    if kwargs.get('tag_name') != None :
        posts = posts.filter(tags__name__in=[kwargs['tag_name']])
    posts = posts.order_by('-published_date', '-id')
    posts = Paginator(posts, 3) 
    try:    
        page_number = request.GET.get('page')
        posts = posts.get_page(page_number)
    except PageNotAnInteger:
        posts = posts.get_page(1)
    except EmptyPage:
        posts = posts.get_page(1)
    context = {'posts':posts}
    return render(request, 'blog/blog-home.html', context)


def blog_single(request, pid):
    post = get_object_or_404(Post.objects.filter(status=1),pk=pid)
    # ---------- login check ----------
    if post.loginrequired and not request.user.is_authenticated:
        messages.error(request,"You must be logged in to view this post.")
        return redirect("accounts:login")
    # ---------- VIEW COUNTER ----------
    if request.user.is_authenticated:
        obj, created = PostView.objects.get_or_create(user=request.user,post=post)
        if created:
            post.counted_view += 1
            post.save(update_fields=["counted_view"])
    else:
        session_key = f"viewed_post_{post.id}"
        if not request.session.get(session_key):
            post.counted_view += 1
            post.save(update_fields=["counted_view"])
            request.session[session_key] = True
    # ---------- COMMENTS ----------
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request,"Your comment has been sent successfully!")
            return redirect("Blog:single", pid=post.id)
        else:
            messages.error(request,"There was an error with your comment. Please try again.")
    else:
        form = CommentForm() 
    comments = Comment.objects.filter(post=post,approved=True)
    context = {"post": post,"comments": comments,"form": form,}
    return render(request,"blog/blog-single.html",context)


def blog_category(request, cat_name):
    # ---------- FILTERING ----------
    posts = Post.objects.filter(status=1)
    posts = posts.filter(category__name=cat_name)
    context = {'posts':posts}
    return render(request, 'blog/blog-home.html', context)


def blog_search(request):
    # --------- FILTERING ----------
    posts = Post.objects.filter(status=1)
    if request.method == 'GET':
        if s := request.GET.get('s'):
            posts = posts.filter(content__contains=s)
    context = {'posts': posts}
    return render(request, 'blog/blog-home.html', context)