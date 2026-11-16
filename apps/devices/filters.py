import django_filters

from apps.devices.models import MicroController

class MicroControllerModelFilterSet(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(field_name="mcm_is_active")


class MicroControllerFilterSet(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(field_name="mc_is_active")