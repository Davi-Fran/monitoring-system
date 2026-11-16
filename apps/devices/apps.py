from django.apps import AppConfig

class AppsConfig(AppConfig):
    name = "apps.devices"

    def ready(self):
        from apps.devices import signals