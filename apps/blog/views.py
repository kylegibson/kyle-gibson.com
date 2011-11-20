from django.shortcuts import render_to_response, get_object_or_404, render

from blog.models import Post

def index(request):
    latest_posts_list = Post.objects.all().order_by('-pub_date')[:5]
    return render(request, 'blog/templates/post_index.haml', locals())

def details(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog/templates/post_details.haml', locals())


