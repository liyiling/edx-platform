"""
Tests for the Theme Redirect Middleware
"""

from mock import patch, Mock
from django.test import TestCase
from ..middleware import ThemeRedirectMiddleware
from django.contrib.redirects.models import Redirect


class TestThemeRedirectMiddlewareProcessRequest(TestCase):
    """
    Test processing a request through the middleware
    """

    def make_request(self, host="", path=""):
        request = Mock()
        request.META = {'HTTP_HOST': host}
        request.path = "{path}".format(path=path)
        return request

    def make_url(self, path):
        return "https://{host}/{path}".format(host=self.host, path=path)

    def setUp(self):
        super(TestThemeRedirectMiddlewareProcessRequest, self).setUp()
        self.host = "foo.com"
        self.middleware = ThemeRedirectMiddleware()
        self.request = self.make_request(self.host, "bar")
        self.dummy_request = self.make_request()

    def test_middleware_called(self):
        with patch.object(ThemeRedirectMiddleware, 'process_request') as mock_method:
            mock_method.return_value = True
            self.middleware.process_request(self.dummy_request)
        self.assertTrue(mock_method.called)

    def test_middleware_with_redirect_url(self):
        with patch('openedx.core.djangoapps.theming.middleware.is_request_in_themed_site', return_value=True):
            with patch.object(self.request, 'is_secure') as mock_method:
                Redirect.objects.create(site_id=1, old_path=self.make_url("bar"), new_path=self.make_url("bar_new"))
                self.middleware.process_request(self.request)
