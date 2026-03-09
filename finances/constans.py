DEFAULT_CATEGORY_TYPE = "expenses"
CATEGORY_TYPES = (
    ("expenses", "Gastos"),
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
TRANSACTION_TYPES = (
    ("expense", "Gasto"),
    ("income", "Ingreso"),
    ("transfer", "Transferencia"),
    ("savings_expense", "Ingreso de Ahorro"),
    ("savings_income", "Gasto de Ahorro"),
)
