from django.conf.urls.defaults import patterns, include, url
from tastypie.api import Api
from blog.api.resources import PostResource

v1_api = Api(api_name='v1')
v1_api.register(PostResource())

urlpatterns = patterns('blog.views',
    url(r'^api/', include(v1_api.urls)),
    url(r'^(?P<post_id>\d+)', 'details', name='blog_details'),
    url(r'^(?P<post_id>\d+)(?P<title_slug>.+)', 'details', name='blog_details'),
    url(r'^$', 'index', name='blog_index'),
)

