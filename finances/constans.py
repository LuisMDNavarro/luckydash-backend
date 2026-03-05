DEFAULT_CATEGORY_TYPE = "expenses"
CATEGORY_TYPES = (
    ("expenses", "Gastos"),
    ("income", "Ingresos"),
)

DEFAULT_ACCOUNT_TYPE = "cash"
ACCOUNT_TYPES = (
    (DEFAULT_ACCOUNT_TYPE, "Efectivo"),
    ("debit", "Debito"),
    ("credit", "Crédito"),
)

DEFAULT_TRANSACTION_TYPE = "expense"
TRANSACTION_TYPES = (
    ("expense", "Gasto"),
    ("income", "Ingreso"),
    ("transfer", "Transferencia"),
    ("savings_expense", "Ingreso de Ahorro"),
    ("savings_income", "Gasto de Ahorro"),
)
