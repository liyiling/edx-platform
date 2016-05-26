from django.conf import settings
from django.core.cache import cache
from django.shortcuts import redirect
from django.contrib.redirects.models import Redirect
from openedx.core.djangoapps.theming.helpers import is_request_in_themed_site


class ThemeRedirectMiddleware(object):
    """
    Redirect users from expired courses' about page to all courses page
    """
    def process_request(self, request):
        """
        Checks request has been made from theme, redirect the user from expired
        courses' about page to all courses page by cache or Redirect Model.
        """
        if is_request_in_themed_site():
            host = request.META['HTTP_HOST']
            redirect_from = ''.join(('http', ('', 's')[request.is_secure()], '://', host, request.path))
            cache_key = "theme_redirect.{host}".format(host=host)
            host_redirects = cache.get(cache_key)
            if host_redirects is None:
                host_redirects = {redirect.old_path: redirect.new_path for redirect in Redirect.objects.filter(
                    old_path__icontains=host)}
                cache.set(cache_key, host_redirects, settings.THEME_REDIRECT_CACHE_TIMEOUT)
            redirect_to = host_redirects.get(redirect_from)
            if redirect_to:
                return redirect(redirect_to)
