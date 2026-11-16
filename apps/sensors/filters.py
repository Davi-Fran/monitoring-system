import django_filters

class SensorModelFilterSet(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(field_name="sm_is_active")


class SensorFilterSet(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(field_name="sen_is_active")
    micro_controller_id = django_filters.NumberFilter(field_name="sen_connected_to")


class SensorReadingFilterSet(django_filters.FilterSet):
    since = django_filters.DateTimeFilter(field_name="sr_measured_at", lookup_expr="gte")
    until = django_filters.DateTimeFilter(field_name="sr_measured_at", lookup_expr="lte")
    sensor_id = django_filters.NumberFilter(field_name="sr_sen")
    laboratory_id = django_filters.NumberFilter(
        field_name="sr_sen__sen_connected_to__mc_laboratory"
    )