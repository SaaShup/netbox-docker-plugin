"""Host API Test Case"""

from unittest import TestCase
from netbox_docker_plugin.templatetags.host import remove_password


class ReplacePasswordTestCase(TestCase):
    """Replace Password function Test Case Class"""

    def test_replace_password(self):
        """Test that replace password works"""
        self.assertEqual(remove_password("http://localhost"), "http://localhost")
        self.assertEqual(remove_password("https://localhost"), "https://localhost")
        self.assertEqual(
            remove_password("http://titi@localhost"), "http://titi@localhost"
        )
        self.assertEqual(
            remove_password("http://titi:@localhost"), "http://titi:@localhost"
        )
        self.assertEqual(
            remove_password("http://titi:toto@localhost"), "http://titi:***@localhost"
        )
