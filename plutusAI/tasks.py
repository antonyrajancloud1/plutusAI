# Celery's autodiscover_tasks() imports this module; it pulls in every module
# that defines @shared_task so the worker registers all of them.
from plutusAI.server import AngelOneApp, base  # noqa: F401
from plutusAI.server.priceAction import priceActionScalper  # noqa: F401
