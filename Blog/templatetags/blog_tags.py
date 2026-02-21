from django import template
from Blog.models import Post, Comment
from Blog.models import Category
from taggit.models import Tag, TaggedItem
from django.contrib.contenttypes.models import ContentType

register = template.Library()

@register.simple_tag(name='totalposts')
def function():
    posts = Post.objects.filter(status=1).count()
    return posts

@register.simple_tag(name='comments_count')
def function(pid):
    return Comment.objects.filter(post=pid, approved=True).count()
    

@register.simple_tag(name='posts')
def function():
    posts = Post.objects.filter(status=1)
    return posts

@register.filter
def snippet(value,arg=20):
    return value[:arg] + '...'

@register.inclusion_tag('blog/blog-popular-posts.html')
def latestposts():
    posts = Post.objects.filter(status=1).order_by('published_date')[:3]
    return {'posts':posts}

@register.inclusion_tag('blog/blog-post-categories.html')
def postcategories():
    posts = Post.objects.filter(status=1)
    categories = Category.objects.all()
    cat_dict = {}
    for name in categories:
        cat_dict[name]=posts.filter(category=name).count()     
    return {'categories':cat_dict}

@register.inclusion_tag('blog/blog-tagcloud.html')
def posttags():
    post_type = ContentType.objects.get_for_model(Post)
    tag_ids = TaggedItem.objects.filter(content_type=post_type).values_list('tag_id', flat=True)
    tags = Tag.objects.filter(id__in=tag_ids).distinct()[:6]
    return {'tags': tags}