from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

import datetime

#class Tag(models.Model):
#    name = models.CharField(max_length=256)
#    posts = models.ManyToManyField(_('Post'))

class Post(models.Model):
    visible   = models.BooleanField(_('Visible'))
    title     = models.CharField(_('Title'), max_length=256)
    author    = models.ForeignKey(User)
    pub_date  = models.DateTimeField(_('Date published'))
    body_mkd  = models.TextField(_('Post body as markdown'))
    body_html = models.TextField(_('Post body as HTML'), blank=True, null=True)
    #tags = models.ManyToManyField(_('Tag'))

    def __unicode__(self):
        return self.title

    def save(self):
        import markdown
        self.body_html = markdown.markdown(self.body_mkd)
        super(Post, self).save()

    def was_published_today(self):
        return self.pub_date.date() == datetime.date.today()

    @models.permalink
    def get_absolute_url(self):
        return ('blog.views.details', [str(self.id)])

    def get_absolute_url_seo(self):
        return "%s-%s" % (self.get_absolute_url(), slugify(self.title))


