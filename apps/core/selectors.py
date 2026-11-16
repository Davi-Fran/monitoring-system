from rest_framework.exceptions import ValidationError

def model_list(
    *, 
    queryset, 
    filterset_class, 
    filters=None,
    order_by_field: str | None = None,
):
    filters = filters or {}

    filterset = filterset_class(filters, queryset=queryset)
    if not filterset.is_valid():
        raise ValidationError(filterset.errors)

    if order_by_field is None:
        return filterset.qs

    return filterset.qs.order_by(order_by_field)