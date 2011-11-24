import functools

from django.views.defaults import page_not_found, server_error

page_not_found = functools.partial(page_not_found, template_name="404.haml")
server_error = functools.partial(server_error, template_name="500.haml")
