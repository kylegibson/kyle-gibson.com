from django.conf.urls.defaults import patterns, include, url
from tastypie.api import Api
from blog.api.resources import PostResource

v1_api = Api(api_name='v1')
v1_api.register(PostResource())

urlpatterns = patterns('blog.views',
    url(r'^api/', include(v1_api.urls)),
    url(r'^(?P<post_id>\d+)', 'details'),
    url(r'^$', 'index'),
)

