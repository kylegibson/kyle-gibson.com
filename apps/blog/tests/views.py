from django.test import TestCase
from django.core.urlresolvers import reverse

class BlogViewsTest(TestCase):
    fixtures = ['blog_views_testdata.json']

    def test_blog_index_status_code(self):
        """It should return 200 good for the blog index"""
        r = self.client.get(reverse('blog_index'))
        self.assertEqual(r.status_code, 200)

    def test_blog_details_status_code_good(self):
        """It should return 200 good when a requested post exists"""
        r = self.client.get(reverse('blog_details', args=[1]))
        self.assertEqual(r.status_code, 200)

    def test_blog_details_status_code_bad(self):
        """It should return 404 error when a requested post does not exist"""
        r = self.client.get(reverse('blog_details', args=[100000]))
        self.assertEqual(r.status_code, 404)

    def test_blog_details_allows_slug_text_after_id(self):
        """
        It should return 200 good when a requested post plus additional text is
        provided with the request
        """
        r = self.client.get(reverse('blog_details', args=[1, "foo-bar-foo-bar-foo-bar"]))
        self.assertEqual(r.status_code, 200)
