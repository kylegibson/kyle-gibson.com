from django.shortcuts import render_to_response

from blog.models import Post

def index(request):
    latest_posts_list = Post.objects.all().order_by('-pub_date')[:5]
    return render_to_response('blog/templates/post_index.haml', 
            {'latest_posts_list' : latest_posts_list })


