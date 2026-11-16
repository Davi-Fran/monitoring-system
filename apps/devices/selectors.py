from rest_framework.exceptions import ValidationError

from apps.core.selectors import model_list
from apps.devices.models import MicroControllerModel, MicroController
from apps.devices.filters import MicroControllerModelFilterSet, MicroControllerFilterSet


def micro_controller_model_list(*, filters=None):
    return model_list(
        queryset=MicroControllerModel.objects.all(),
        filterset_class=MicroControllerModelFilterSet,
        filters=filters,
        order_by_field="mcm_name"
    )


def micro_controller_list(*, filters=None):
    return model_list(
        queryset=MicroController.objects.all(),
        filterset_class=MicroControllerFilterSet,
        filters=filters,
        order_by_field="mc_id",
    )


def micro_controller_retrieve():
    return model_list(
        queryset=MicroController.objects.select_related("mc_model", "mc_laboratory"),
        filterset_class=MicroControllerFilterSet,
    )