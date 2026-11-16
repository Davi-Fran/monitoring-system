from django.db.models import Prefetch

from rest_framework.exceptions import ValidationError

from apps.core.selectors import model_list
from apps.laboratories.models import Laboratory
from apps.laboratories.filters import LaboratoryFilterSet

def laboratory_list(*, filters=None):
    return model_list(
        queryset=Laboratory.objects.all(),
        filterset_class=LaboratoryFilterSet,
        filters=filters,
        order_by_field="lab_name"
    )


def laboratory_retrieve():
    return model_list(
        queryset=Laboratory.objects.prefetch_related("lab_installed_mcs"),
        filterset_class=LaboratoryFilterSet,
    )