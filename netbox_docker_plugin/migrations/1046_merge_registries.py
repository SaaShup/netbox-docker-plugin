# pylint: disable=C0103
"""Migration file: merge registries sharing the same name across hosts"""

import django.db.models.deletion
from django.db import migrations, models


def _has_credentials(registry):
    return bool(registry.username or registry.password)


def merge_duplicate_registries(apps, schema_editor):  # pylint: disable=W0613
    """
    Merge registries sharing the same name into a single one.

    The kept registry is the oldest one holding credentials, or the oldest one
    if none does. Images of the discarded registries are moved to the kept one.
    """

    Registry = apps.get_model("netbox_docker_plugin", "Registry")
    Image = apps.get_model("netbox_docker_plugin", "Image")
    ContentType = apps.get_model("contenttypes", "ContentType")
    TaggedItem = apps.get_model("extras", "TaggedItem")
    JournalEntry = apps.get_model("extras", "JournalEntry")

    names = (
        Registry.objects.values("name")
        .annotate(count=models.Count("id"))
        .filter(count__gt=1)
        .values_list("name", flat=True)
    )

    content_type = ContentType.objects.filter(
        app_label="netbox_docker_plugin", model="registry"
    ).first()

    for name in names:
        registries = list(Registry.objects.filter(name=name).order_by("id"))
        keeper = next(
            (registry for registry in registries if _has_credentials(registry)),
            registries[0],
        )
        discarded = [registry for registry in registries if registry.pk != keeper.pk]
        discarded_ids = [registry.pk for registry in discarded]

        for registry in discarded:
            if _has_credentials(registry) and (
                registry.serveraddress != keeper.serveraddress
                or registry.username != keeper.username
                or registry.password != keeper.password
                or registry.email != keeper.email
            ):
                print(
                    f"\n  Registry '{name}' (id {registry.pk}) merged into id {keeper.pk}: "
                    "its server address or credentials differ and are discarded."
                )

        Image.objects.filter(registry_id__in=discarded_ids).update(registry=keeper)

        if content_type is not None:
            TaggedItem.objects.filter(
                content_type=content_type, object_id__in=discarded_ids
            ).delete()
            JournalEntry.objects.filter(
                assigned_object_type=content_type,
                assigned_object_id__in=discarded_ids,
            ).delete()

        Registry.objects.filter(pk__in=discarded_ids).delete()


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("extras", "0001_initial"),
        ("netbox_docker_plugin", "1045_image_tenant_image_tenant_group"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="registry",
            name="netbox_docker_plugin_registry_name_host",
        ),
        migrations.AlterField(
            model_name="image",
            name="registry",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="images",
                to="netbox_docker_plugin.registry",
            ),
        ),
        migrations.RunPython(
            merge_duplicate_registries, reverse_code=migrations.RunPython.noop
        ),
    ]
