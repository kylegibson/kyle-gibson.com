from django.conf.urls.defaults import patterns, include, url
from django.views.generic import RedirectView
from django.contrib import admin

handler404 = 'views.page_not_found'
handler500 = 'views.server_error'

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/blog')),
    url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
