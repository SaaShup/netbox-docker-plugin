"""Plugin Initialization Test Case"""

import json
from django.urls import reverse
from utilities.testing.api import APITestCase


class InitTestCase(APITestCase):
    """Plugin Initialization Test Case Class"""

    def test_that_plugin_is_loaded(self):
        """Test that the plugin is loaded"""
        url = reverse("plugins-api:netbox_docker-api:api-root")
        response = self.client.get(f"{url}?format=json", **self.header)

        content = json.loads(response.content)

        self.assertTrue("hosts" in content)
        self.assertTrue("images" in content)
        self.assertEqual(response.status_code, 200)
