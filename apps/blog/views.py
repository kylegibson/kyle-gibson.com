from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from blog.models import Post

def index(request):
    latest_posts_list = Post.objects.all().order_by('-pub_date')[:5]
    return render_to_response('blog/templates/post_index.haml', 
            {'latest_posts_list' : latest_posts_list},
            context_instance=RequestContext(request))

def details(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render_to_response('blog/templates/post_details.haml',
            {'post' : post},
            context_instance=RequestContext(request))



