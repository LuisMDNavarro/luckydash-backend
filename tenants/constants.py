DEFAUL_SUBSCRIPTION = "free"
SUBSCRIPTION_TYPES = (
    (DEFAUL_SUBSCRIPTION, "Gratis"),
    ("free_test", "Prueba gratuita"),
    ("paid", "Pago"),
)

DEFAULT_ROLE = "member"
ROLE_CHOICES = (
    ("owner", "Propietario"),
    ("admin", "Administrador"),
    (DEFAULT_ROLE, "Miembro"),
)
