import django_filters

class LaboratoryFilterSet(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(field_name="lab_is_active")