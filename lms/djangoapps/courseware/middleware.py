"""
Middleware for the courseware app
"""

from django.conf import settings
from django.core.cache import cache
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.redirects.models import Redirect
from openedx.core.djangoapps.theming.helpers import is_request_in_themed_site
from courseware.courses import UserNotEnrolled


class RedirectUnenrolledMiddleware(object):
    """
    Catch UserNotEnrolled errors thrown by `get_course_with_access` and redirect
    users to the course about page
    """
    def process_exception(self, _request, exception):
        if isinstance(exception, UserNotEnrolled):
            course_key = exception.course_key
            return redirect(
                reverse(
                    'courseware.views.views.course_about',
                    args=[course_key.to_deprecated_string()]
                )
            )


class RedirectExpiredCoursesMiddleware(object):

    def process_request(self, request):
        if is_request_in_themed_site():
            redirect_from = ''.join(
                ('http', ('', 's')[request.is_secure()], '://', request.META['HTTP_HOST'], request.path)
            )
            cache_key = "redirect.{url}".format(url=redirect_from)
            redirect_to = cache.get(cache_key, '')
            if not redirect_to:
                redirect_object = Redirect.objects.filter(old_path=redirect_from)
                if len(redirect_object) > 0:
                    redirect_to = redirect_object[0].new_path
                    cache.set(cache_key, redirect_to, settings.REDIRECT_URL_CACHE_TIMEOUT)
            if redirect_to:
                return redirect(redirect_to)
