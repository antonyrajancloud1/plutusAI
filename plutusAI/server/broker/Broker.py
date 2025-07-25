from plutusAI.server.base import *
from plutusAI.server.broker.AngelOneBroker import AngelOneBroker
from plutusAI.server.broker.exness.ExnessBroker import ExnessBroker
from plutusAI.server.constants import *


class Broker:
    def __init__(self, user_email,index_group):
        self.user_broker_data = BrokerDetails.objects.filter(user_id=user_email, index_group=index_group)
        self.user_broker_details = list(self.user_broker_data.values())
        if len(self.user_broker_details) > 0:
            self.user_broker_details = self.user_broker_details[0]
            user_broker = self.user_broker_details[BROKER_NAME]
            self.is_demo_enabled = bool(self.user_broker_details[IS_DEMO_TRADING_ENABLED])
            match user_broker:
                case "angel_one":
                    self.BrokerObject = AngelOneBroker(self.user_broker_data)
                case "kite":
                    addLogDetails(INFO, "kite")
                case "exness":
                    self.BrokerObject =ExnessBroker(user_email)