"""
Test cms startup
"""

from django.conf import settings

from django.test import TestCase
from django.test.utils import override_settings

from path import Path
from mock import patch
from cms.startup import run

RED_THEME_DIR = Path("/edx/app/edxapp/edx-platform/themes/red-theme")


class StartupTestCase(TestCase):
    """
    Test cms startup
    """

    def setUp(self):
        super(StartupTestCase, self).setUp()

    @override_settings(COMPREHENSIVE_THEME_DIR=RED_THEME_DIR)
    def test_run_with_theme(self):
        self.assertEqual(settings.COMPREHENSIVE_THEME_DIR, RED_THEME_DIR)
        with patch('cms.startup.enable_comprehensive_theme') as mock_enable_comprehensive_theme:
            run()
            self.assertTrue(mock_enable_comprehensive_theme.called)

    @override_settings(COMPREHENSIVE_THEME_DIR="")
    def test_run_without_theme(self):
        self.assertEqual(settings.COMPREHENSIVE_THEME_DIR, "")
        with patch('cms.startup.enable_comprehensive_theme') as mock_enable_comprehensive_theme:
            run()
            self.assertFalse(mock_enable_comprehensive_theme.called)

    @override_settings(COMPREHENSIVE_THEME_DIR=RED_THEME_DIR)
    @override_settings(STATICFILES_DIRS=[])
    @override_settings(LOCALE_PATHS=())
    @patch.dict("django.conf.settings.DEFAULT_TEMPLATE_ENGINE", {
        "DIRS": [],
    })
    def test_enable_comprehensive_theme(self):

        with patch('openedx.core.djangoapps.theming.core.Path.isdir') as mock_isdir:
            mock_isdir.return_value = True
            # Run startup script
            run()
            self.assertIn(
                RED_THEME_DIR / "cms/templates",
                settings.DEFAULT_TEMPLATE_ENGINE['DIRS'],
            )
            self.assertIn(
                RED_THEME_DIR / "cms/static",
                settings.STATICFILES_DIRS,
            )
            self.assertIn(
                RED_THEME_DIR / "cms/conf/locale",
                settings.LOCALE_PATHS,
            )

    @override_settings(COMPREHENSIVE_THEME_DIR="")
    def test_disabled_comprehensive_theme(self):

        with patch('openedx.core.djangoapps.theming.core.Path.isdir') as mock_isdir:
            mock_isdir.return_value = True
            # Run cms startup script
            run()
            self.assertNotIn(
                RED_THEME_DIR / "cms/templates",
                settings.DEFAULT_TEMPLATE_ENGINE['DIRS'],
            )
            self.assertNotIn(
                RED_THEME_DIR / "cms/static",
                settings.STATICFILES_DIRS,
            )
            self.assertNotIn(
                RED_THEME_DIR / "cms/conf/locale",
                settings.LOCALE_PATHS,
            )
