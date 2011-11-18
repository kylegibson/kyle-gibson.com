from blog.models import Post
from django.contrib import admin

class PostAdmin(admin.ModelAdmin):
    list_display    = ('visible', 'title', 'pub_date', 'author')
    list_filter     = ['pub_date']
    search_fields   = ['title', 'body_mkd']
    date_hierarchy  = 'pub_date'

admin.site.register(Post, PostAdmin)
