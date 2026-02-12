from django.contrib import admin
from Blog.models import Post
# Register your models here.
# @admin.register(Post)
class PostAmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'
    # fields = ('title',)
    list_display = ('id','title', 'status', 'counted_view')
    list_filter = ('status',)
    # ordering = ['created_date']
    search_fields = ['title', 'content']
admin.site.register(Post, PostAmin)