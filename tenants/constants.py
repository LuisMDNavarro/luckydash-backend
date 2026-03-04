DEFAUL_SUBSCRIPTION = "free"
TEST_SUBSCRIPTION = "free_test"
PAID_SUBSCRIPTION = "paid"

SUBSCRIPTION_TYPES = (
    (DEFAUL_SUBSCRIPTION, "Gratis"),
    (TEST_SUBSCRIPTION, "Prueba gratuita"),
    (PAID_SUBSCRIPTION, "Pago"),
)

DEFAULT_ROLE = "member"
OWNER_ROLE = "owner"
ROLE_CHOICES = (
    (OWNER_ROLE, "Propietario"),
    ("admin", "Administrador"),
    (DEFAULT_ROLE, "Miembro"),
)

SUBSCRIPTION_LIMITS = {
    DEFAUL_SUBSCRIPTION: {
        "cards": 3,
    },
    TEST_SUBSCRIPTION: {
        "cards": 5,
    },
    PAID_SUBSCRIPTION: {
        "cards": None,
    },
}
