"""Utilities init"""

# pylint: disable=C0301
webhooks = [
    {
        "name": "[Docker] Add container",
        "content_types": "container",
        "enabled": True,
        "type_create": True,
        "type_update": False,
        "type_delete": False,
        "type_job_start": False,
        "type_job_end": False,
        "http_method": "POST",
        "payload_url": "{{ data.host.endpoint }}/api/engine/containers",
        "ssl_verification": False,
    },
    {
        "name": "[Docker] Add host",
        "content_types": "host",
        "enabled": True,
        "type_create": True,
        "type_update": False,
        "type_delete": False,
        "type_job_start": False,
        "type_job_end": False,
        "http_method": "GET",
        "payload_url": "{{ data.endpoint }}/api/engine/endpoint?id={{ data.id }}&token={{ data.token.key }}&endpoint={{ data.endpoint }}&url={{ data.netbox_base_url }}",
        "ssl_verification": False,
    },
    {
        "name": "[Docker] Add image",
        "content_types": "image",
        "enabled": True,
        "type_create": True,
        "type_update": False,
        "type_delete": False,
        "type_job_start": False,
        "type_job_end": False,
        "http_method": "POST",
        "payload_url": "{{ data.host.endpoint }}/api/engine/images",
        "ssl_verification": False,
    },
    {
        "name": "[Docker] Add network",
        "content_types": "network",
        "enabled": True,
        "type_create": True,
        "type_update": False,
        "type_delete": False,
        "type_job_start": False,
        "type_job_end": False,
        "http_method": "POST",
        "payload_url": "{{ data.host.endpoint }}/api/engine/networks",
        "ssl_verification": False,
    },
    {
        "name": "[Docker] Add volume",
        "content_types": "volume",
        "enabled": True,
        "type_create": True,
        "type_update": False,
        "type_delete": False,
        "type_job_start": False,
        "type_job_end": False,
        "http_method": "POST",
        "payload_url": "{{ data.host.endpoint }}/api/engine/volumes",
        "ssl_verification": False,
    },
    {
        "name": "[Docker] Delete container",
        "content_types": "container",
        "enabled": True,
        "type_create": False,
        "type_update": False,
        "type_delete": True,
        "type_job_start": False,
        "type_job_end": False,
        "http_method": "DELETE",
        "payload_url": "{{ data.host.endpoint }}/api/engine/containers",
        "ssl_verification": False,
    },
    {
        "name": "[Docker] Delete host",
        "content_types": "host",
        "enabled": True,
        "type_create": False,
        "type_update": False,
        "type_delete": True,
        "type_job_start": False,
        "type_job_end": False,
        "http_method": "DELETE",
        "payload_url": "{{ data.endpoint }}/api/engine/endpoint",
        "ssl_verification": False,
    },
    {
        "name": "[Docker] Delete image",
        "content_types": "image",
        "enabled": True,
        "type_create": False,
        "type_update": False,
        "type_delete": True,
        "type_job_start": False,
        "type_job_end": False,
        "http_method": "DELETE",
        "payload_url": "{{ data.host.endpoint }}/api/engine/images",
        "ssl_verification": False,
    },
    {
        "name": "[Docker] Delete network",
        "content_types": "network",
        "enabled": True,
        "type_create": False,
        "type_update": False,
        "type_delete": True,
        "type_job_start": False,
        "type_job_end": False,
        "http_method": "DELETE",
        "payload_url": "{{ data.host.endpoint }}/api/engine/networks",
        "ssl_verification": False,
    },
    {
        "name": "[Docker] Delete volume",
        "content_types": "volume",
        "enabled": True,
        "type_create": False,
        "type_update": False,
        "type_delete": True,
        "type_job_start": False,
        "type_job_end": False,
        "http_method": "DELETE",
        "payload_url": "{{ data.host.endpoint }}/api/engine/volumes",
        "ssl_verification": False,
    },
    {
        "name": "[Docker] Modify host",
        "content_types": "host",
        "enabled": True,
        "type_create": False,
        "type_update": True,
        "type_delete": False,
        "type_job_start": False,
        "type_job_end": False,
        "http_method": "POST",
        "payload_url": "{{ data.endpoint }}/api/engine/endpoint",
        "ssl_verification": False,
    },
    {
        "name": "[Docker] Modify image",
        "content_types": "image",
        "enabled": True,
        "type_create": False,
        "type_update": True,
        "type_delete": False,
        "type_job_start": False,
        "type_job_end": False,
        "http_method": "POST",
        "payload_url": "{{ data.host.endpoint }}/api/engine/images",
        "ssl_verification": False,
    },
    {
        "name": "[Docker] Modify container",
        "content_types": "container",
        "enabled": True,
        "type_create": False,
        "type_update": True,
        "type_delete": False,
        "type_job_start": False,
        "type_job_end": False,
        "http_method": "PUT",
        "payload_url": "{{ data.host.endpoint }}/api/engine/containers",
        "ssl_verification": False,
    },
]


# pylint: disable=W0613
def create_webhook(app_config, **kwargs):
    """Create automatically plugin webhook"""
    if app_config.label == "netbox_docker_plugin":
        # pylint: disable=C0415
        from django.contrib.contenttypes.models import ContentType
        from extras.models import Webhook

        if "eventrule" in app_config.apps.all_models["extras"]:
            # pylint: disable=E0611
            from extras.models import EventRule

            wh_content_type = ContentType.objects.get(
                app_label="extras", model="webhook"
            )

            for webhook in webhooks:
                results = Webhook.objects.filter(name=webhook["name"])
                if len(results) == 0:
                    obj = Webhook(
                        name=webhook["name"],
                        description="Added automatically by the Netbox Docker Plugin",
                        http_method=webhook["http_method"],
                        payload_url=webhook["payload_url"],
                        ssl_verification=webhook["ssl_verification"],
                    )
                    obj.save()

                    event_types = []

                    if webhook["type_create"]:
                        event_types.append("object_created")

                    if webhook["type_update"]:
                        event_types.append("object_updated")

                    if webhook["type_delete"]:
                        event_types.append("object_deleted")

                    if webhook["type_job_start"]:
                        event_types.append("job_started")

                    if webhook["type_job_end"]:
                        event_types.append("job_completed")

                    eventrule = EventRule(
                        name=webhook["name"],
                        description="Added automatically by the Netbox Docker Plugin",
                        event_types=event_types,
                        action_object_id=obj.pk,
                        action_object_type=wh_content_type,
                    )
                    eventrule.save()

                    obj_content_type = ContentType.objects.get(
                        app_label="netbox_docker_plugin", model=webhook["content_types"]
                    )

                    # pylint: disable=E1101
                    eventrule.object_types.set([obj_content_type.pk])
                    eventrule.save()

            return

        for webhook in webhooks:
            results = Webhook.objects.filter(
                payload_url=webhook["payload_url"],
                type_create=webhook["type_create"],
                type_update=webhook["type_update"],
                type_delete=webhook["type_delete"],
            )

            if len(results) == 0:
                obj = Webhook(
                    name=webhook["name"],
                    type_create=webhook["type_create"],
                    type_update=webhook["type_update"],
                    type_delete=webhook["type_delete"],
                    type_job_start=webhook["type_job_start"],
                    type_job_end=webhook["type_job_end"],
                    http_method=webhook["http_method"],
                    payload_url=webhook["payload_url"],
                    ssl_verification=webhook["ssl_verification"],
                )
                obj.save()

                content_type = ContentType.objects.get(
                    app_label="netbox_docker_plugin", model=webhook["content_types"]
                )

                # pylint: disable=E1101
                obj.content_types.set([content_type.pk])
                obj.save()
