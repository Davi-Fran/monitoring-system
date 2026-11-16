from django.core.validators import RegexValidator

mac_address_validator = RegexValidator(
    regex=r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$",
    message="The mac address must be in the following pattern: e.g., \"02:82:66:00:00:0A\"",
    code="invalid_mac_address",
)