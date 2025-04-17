from django.views.decorators.http import require_http_methods

from .server.manualOrder import *


# Create your tests here.
@require_http_methods([GET])
def tester(request):
    # data = json.loads(request.body)
    print("tester")
    user_id =get_user_email(request)
    print(user_id)
    try:
        for order_data in manual_orders_sample_data:
            order = order_data.copy()
            order["user_id"] = user_id
            add_manual_order(order)
    except Exception as e:
        print(e)