from app.api.customer import bp as bp_api_customer
from app.api.income import IncomeAPI
from app.api.trade import bp as bp_api_trade
from app.api.user import bp as bp_api_user

router = [
    bp_api_user,
    bp_api_customer,
    IncomeAPI,
    bp_api_trade
]
