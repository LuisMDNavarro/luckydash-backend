from django.core.validators import RegexValidator

hex_color_validator = RegexValidator(
    regex=r"^#(?:[0-9a-fA-F]{3}){1,2}$",
    message="El color debe ser un código HEX válido como #FFF ó #FFFFFF",
)
