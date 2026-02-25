from django.contrib import admin
from Blog.models import Post, Category, Comment
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.
# @admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'
    # fields = ('title',)
    list_display = ('id','title', 'author', 'loginrequired','status', 'counted_view', 'published_date', 'created_date')
    list_filter = ('status', 'author',)
    # ordering = ['created_date']
    search_fields = ['title', 'content']
    ordering = ('-counted_view', '-published_date',)
    summernote_fields = ('content',)

class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'
    list_display = ('name','approved', 'post', 'created_date')
    list_filter = ('post', 'approved',)
    search_fields = ['name', 'post']

admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)