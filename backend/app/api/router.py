from app.api.client import bp as bp_api_client
from app.api.income import bp as bp_api_income
from app.api.trade import bp as bp_api_trade
from app.api.user import bp as bp_api_user

router = [
    bp_api_user,
    bp_api_client,
    bp_api_income,
    bp_api_trade
]
