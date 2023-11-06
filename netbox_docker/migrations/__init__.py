"""Migrations base functions"""

from django.db import models
import taggit.managers
import utilities.json


def netbox_common_fields() -> list:
    """Returns netbox common fields"""
    return [
        (
            "id",
            models.BigAutoField(auto_created=True, primary_key=True, serialize=False),
        ),
        ("created", models.DateTimeField(auto_now_add=True, null=True)),
        ("last_updated", models.DateTimeField(auto_now=True, null=True)),
        (
            "custom_field_data",
            models.JSONField(
                blank=True,
                default=dict,
                encoder=utilities.json.CustomFieldJSONEncoder,
            ),
        ),
        (
            "tags",
            taggit.managers.TaggableManager(
                through="extras.TaggedItem", to="extras.Tag"
            ),
        ),
    ]
