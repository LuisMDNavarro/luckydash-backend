DEFAULT_CATEGORY_TYPE = "expense"
CATEGORY_TYPES = (
    (DEFAULT_CATEGORY_TYPE, "Gastos"),
    ("income", "Ingresos"),
)

DEFAULT_ACCOUNT_TYPE = "cash"
DEBIT_TYPE = "debit"
CREDIT_TYPE = "credit"
ACCOUNT_TYPES = (
    (DEFAULT_ACCOUNT_TYPE, "Efectivo"),
    (DEBIT_TYPE, "Debito"),
    (CREDIT_TYPE, "Crédito"),
)

DEFAULT_TRANSACTION_TYPE = "expense"
TRANSFER_TRANSACTION_TYPE = "transfer"
INSTALLMENTS_TRANSACTION_TYPE = "installments_expense"
TRANSACTION_TYPES = (
    (DEFAULT_TRANSACTION_TYPE, "Gasto"),
    (INSTALLMENTS_TRANSACTION_TYPE, "Gasto a Cuotas"),
    ("income", "Ingreso"),
    (TRANSFER_TRANSACTION_TYPE, "Transferencia"),
    ("savings_expense", "Ingreso de Ahorro"),
    ("savings_income", "Gasto de Ahorro"),
)
MIN_INSTALLMENTS = 2
MAX_INSTALLMENTS = 12
