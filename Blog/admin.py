from django.contrib import admin
from Blog.models import Post, Category
# Register your models here.
# @admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'
    # fields = ('title',)
    list_display = ('id','title', 'author', 'status', 'counted_view', 'published_date', 'created_date')
    list_filter = ('status', 'author',)
    # ordering = ['created_date']
    search_fields = ['title', 'content']
    ordering = ('-published_date',)
    
admin.site.register(Category)
admin.site.register(Post, PostAdmin)