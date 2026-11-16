from django.apps import AppConfig

class AppsConfig(AppConfig):
    name = "apps.sensors"

    def ready(self):
        from apps.sensors import signals