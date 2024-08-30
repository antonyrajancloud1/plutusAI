# ADMIN_USER_ID="user1@gmail.com"
ADMIN_USER_ID='madara@plutus.com'
SOCKET_JOB="socket_job"
HTTP_JOB="http_job"

SOCKET_JOB_TYPE='3'
### strategy ###
STRATEGY_HUNTER='hunter'
STRATEGY_SCALPER='scalper'
STRATEGY_MANUAL='manual'

### index details 
NIFTY_50='Nifty 50'
NIFTY_BANK='Nifty Bank'
NIFTY_FIN_SERVICE='Nifty Fin Service'
#### HTTP METHODS ###
POST = "POST"
GET = "GET"
PUT = "PUT"


#### URLS ####

DEFAULT_PAGE_URL = "NEED TO ADD DEFAULT PAGE"
HOME_PAGE_URL = "home.html"
HOME_URL = "home"
LOGIN_URL = "login"
LOGIN_PAGE_URL = "login.html"
LOGOUT_URL = "logout"
GET_CONFIG_VALUES = "get_config_values"
ADD_USER = "add_user"
UPDATE_CONFIG_VALUES = "update_config_values"
GET_BROKER_DETAILS = "get_broker_details"
ADD_BROKER_DETAILS = "add_broker_details"
EDIT_BROKER_DETAILS = "edit_broker_details"
GET_ORDER_BOOK_DETAILS = "get_order_book_details"
INVALID_URL_PAGE = "invaid_url.html"
INTERNAL_ERROR_PAGE = "internal_error.html"
START_INDEX = "start_index"
STOP_INDEX = "stop_index"
PLANS = "plans"
EDIT_PLAN = "edit_plans"
START_WS = "start_ws"
STOP_WS = "stop_ws"
DASHBOARD='dashboard'
UPDATE_SCALPER = "update_scalper_details"
GET_SCALPER_VALUES = "get_scalper_details"
ADMIN_CONSOLE="admin_console"
CHECK_TASK_STATUS="check_task_status"
BUY_MANUAL="buy_manual"
REGENERATE_TOKEN = "regenrate_token"
#### DATA CONSTANTS ####
ID = "id"
USER_NAME = "user_name"
PASSWORD = "password"
USER_ID = "user_id"
INDEX_NAME = "index_name"
INITIAL_SL = "initial_sl"
IS_SL_REQUIRED = "is_place_sl_required"
SAFE_SL = "safe_sl"
TARGET_FOR_SAFE_SL = "target_for_safe_sl"
TRAILING_POINTS = "trailing_points"
TREND_CHECK_POINTS = "trend_check_points"
LEVELS = "levels"
START_SCHEDULER = "start_scheduler"
BROKER_USER_ID = "broker_user_id"
BROKER_USER_NAME = "broker_user_name"
BROKER_NAME = "broker_name"
BROKER_MPIN = "broker_mpin"
BROKER_API_TOKEN = "broker_api_token"
BROKER_QR = "broker_qr"
INDEX_GROUP = "index_group"
TOKEN='token'

#### INDEX TYPES
INDIAN_INDEX = "indian_index"
FOREX_INDEX = "forex_index"
IS_DEMO_TRADING_ENABLED = "is_demo_trading_enabled"
SCRIPT_NAME = "script_name"
QTY = "qty"
ENTRY_PRICE = "entry_price"
EXIT_PRICE = "exit_price"
EXIT_TIME = "exit_time"
TOTAL='total'
LOTS = "lots"
LTP = "ltp"
CLOSE="close"
CURRENT_EXPIRY = "current_expiry"
NEXT_EXPIRY = "next_expiry"
STRIKE = "strike"
ORDER_PLACED = "order_placed"
ORDER_EXITED = "order_exited"
TARGET="target"
ON_CANDLE_CLOSE="on_candle_close"
TOKEN_GENERATED="token_generated"
TASK_STATUS="task_status"
#### MESSSAGE CONSTANTS ####

STATUS = "status"
SUCCESS = "success"
ERROR = "error"
MESSAGE = "message"
LOGIN_SUCCESS = "login_success"
FAILED = "failed"
LOGIN_ERROR = "error_in_login"
LOGOUT_SUCCESS = "logout_success"
LOGOUT_ERROR = "logout_error"
ALL_CONFIG_VALUES = "all_config_values"
CONFIG_VALUES = "config_values"
CONFIG_VALUES_UPDATED = "config_values_updated"
UNAUTHORISED = "unauthorised"
USER_EXISTS = "user_already_present"
USER_ADDED = "user_added"
INVALID_JSON = "invalid_json"
GLOBAL_ERROR = "internal_error"
INDEX_NOT_FOUND = "index_details_not_found"
BROKER_DETAILS = "broker_details"
BROKER_DETAILS_ADDED = "broker_details_added"
BROKER_DETAILS_UPDATED= "broker_details_updated"
SCALPER_VALUES_UPDATED = "scalper_details_updated"
ORDER_PRESENT="order_present"

ORDER_BOOK_DETAILS = "order_book_details"
PLAN_DETAILS = "plan_details"
STRATEGY='strategy'
SCALPER='scalper'
NSE_OPEN_TIME = "09:15"
START_SCALPER= "start_scalper"
STOP_SCALPER="stop_scalper"
BANKNIFTY_FUTURES='BANKNIFTY25SEP24FUT'
#### INDEX DEFAULT VALUES ####
NIFTY_DEFAULT_VALUES = {
    "index_name": "nifty",
    "initial_sl": "10",
    "is_place_sl_required": True,
    "safe_sl": "10",
    "target_for_safe_sl": "10",
    "trailing_points": "10",
    "trend_check_points": "15",
    "levels": "update levels",
    "user_id": "replace_user_id",
    "start_scheduler": False,
    "stage": "stopped",
    "strike": "100",
    "lots": "10",
}
BANK_NIFTY_DEFAULT_VALUES = {
    "index_name": "bank_nifty",
    "initial_sl": "30",
    "is_place_sl_required": True,
    "safe_sl": "10",
    "target_for_safe_sl": "30",
    "trailing_points": "20",
    "trend_check_points": "50",
    "levels": "update levels",
    "user_id": "replace_user_id",
    "start_scheduler": False,
    "stage": "stopped",
    "strike": "200",
    "lots": "10",
}
FINNIFTY_DEFAULT_VALUES = {
    "index_name": "fin_nifty",
    "initial_sl": "10",
    "is_place_sl_required": True,
    "safe_sl": "10",
    "target_for_safe_sl": "10",
    "trailing_points": "10",
    "trend_check_points": "15",
    "levels": "update levels",
    "user_id": "replace_user_id",
    "start_scheduler": False,
    "stage": "stopped",
    "strike": "100",
    "lots": "10",
}
MIDCAP_DEFAULT_VALUES = {
    "index_name": "midcap_nifty",
    "initial_sl": "10",
    "is_place_sl_required": True,
    "safe_sl": "10",
    "target_for_safe_sl": "10",
    "trailing_points": "10",
    "trend_check_points": "15",
    "levels": "update levels",
    "user_id": "replace_user_id",
    "start_scheduler": False,
    "stage": "stopped",
    "strike": "100",
    "lots": "10",
}
ANGEL_ONE = "angel_one"
AVAILABLE_BROKERS = {INDIAN_INDEX: [ANGEL_ONE, "kite"], "forex": ["exness"]}
STAGE_INITIATED = {"status": "initiated"}
STAGE_STARTED = {"status": "started"}
STAGE_STOPPED = {"status": "stopped"}
STAGE_LONG = {"status": "long_placed"}
STAGE_SHORT = {"status": "short_placed"}
STAGE_BROKER_NOT_PRESENT = {"stage": "broker_not_present"}
# NIFTY_50 = "Nifty 50"
### Broker Param Values #### ANGLEONE ###
VARIETY = "variety"
TRADING_SYMBOL = "tradingsymbol"
SYMBOL_TOKEN = "symboltoken"
EXCHANGE = "exchange"
ORDER_TYPE = "ordertype"
PRODUCT_TYPE = "producttype"
DURATION = "duration"
QUANTITY = "quantity"
TRANSACTION_TYPE = "transactiontype"
NORMAL = "NORMAL"
BUY = "BUY"
SELL = "SELL"
NSE = "NSE"
NFO = "NFO"
MARKET = "MARKET"
INTRADAY = "INTRADAY"
DAY = "DAY"
ORDER_TYPE_SL = "STOPLOSS_LIMIT"
PRICE = "price"
TRIGGER_PRICE = "triggerprice"
ORDERID = "orderid"
STOPLOSS = "STOPLOSS"

##error messages
INCORRECT_INPUT = "Invalid Entries Found For Field "

### LOGGER INFO ###
INFO='info'
ERROR='error'
CONNECTION_ERROR="Internet connection issue"