from user.user_controller import user_router
from account.account_controller import account_router
from transaction.transaction_controller import transaction_router
from auth.auth_controller import auth_router


def register_routes(app):
    app.include_router(user_router, prefix="/user")
    app.include_router(auth_router, prefix="/auth")
    app.include_router(account_router, prefix="/account")
    app.include_router(transaction_router, prefix="/transactions")
    

