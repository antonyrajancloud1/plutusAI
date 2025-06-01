from django.views.decorators.http import require_http_methods
from concurrent.futures import ThreadPoolExecutor, as_completed
from .server.manualOrder import *

# Create your tests here.
@require_http_methods([GET])
def tester(request):
    user_email = get_user_email(request)
    open_orders = OrderBook.objects.filter(user_id=user_email, exit_price__isnull=True)
    broker = Broker(user_email, INDIAN_INDEX).BrokerObject

    # Prepare order data as dicts for easier parallel processing
    order_dicts = []
    for order in open_orders:
        order_dicts.append({
            "entry_time": order.entry_time,
            "exit_time": order.exit_time,
            "script_name": order.script_name,
            "qty": order.qty,
            "entry_price": order.entry_price,
            "exit_price": order.exit_price,
            "status": order.status,
            "total": order.total,
            "strategy": order.strategy,
            "index_name": order.index_name,
        })

    # Worker function: do NOT modify broker.getLtpForPremium itself
    def get_ltp_for_order(order):
        option_details = broker.getCurrentPremiumDetails(NFO, order["script_name"])
        ltp = broker.getLtpForPremium(option_details)  # using the same call
        order["ltp"] = ltp
        return order

    orders_with_ltp = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(get_ltp_for_order, order) for order in order_dicts]
        for future in as_completed(futures):
            orders_with_ltp.append(future.result())

    return JsonResponse(orders_with_ltp, safe=False)