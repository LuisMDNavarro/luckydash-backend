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
ADMIN_ROLE = "admin"
ROLE_CHOICES = (
    (OWNER_ROLE, "Propietario"),
    (ADMIN_ROLE, "Administrador"),
    (DEFAULT_ROLE, "Miembro"),
)

READ_ACTIONS = ["list", "retrieve"]
EDIT_ACTIONS = ["create", "update", "partial_update", "destroy"]
READ_ROLES = [OWNER_ROLE, ADMIN_ROLE, DEFAULT_ROLE]
EDIT_ROLES = [OWNER_ROLE, ADMIN_ROLE]

SUBSCRIPTION_LIMITS = {
    DEFAUL_SUBSCRIPTION: {
        "tenants": 1,
        "memberships": 3,
        "accounts": 3,
        "categories": 10,
        "tickets": False,
    },
    TEST_SUBSCRIPTION: {
        "tenants": 1,
        "memberships": 3,
        "accounts": None,
        "categories": None,
        "tickets": True,
    },
    PAID_SUBSCRIPTION: {
        "tenants": None,
        "memberships": None,
        "accounts": None,
        "categories": None,
        "tickets": True,
    },
}
