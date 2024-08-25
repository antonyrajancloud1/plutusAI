from django.http import JsonResponse
from plutusAI.server.constants import *
from plutusAI.server.supportResistance.AngelOneSR import SupportResistanceCalculator
def testerCheck(request):
    calculator = SupportResistanceCalculator("antonyrajan.d@gmail.com", INDIAN_INDEX,100)
    levels = calculator.fetch_support_resistance(NIFTY_BANK, "ONE_HOUR",60)

    # print(levels)
    return JsonResponse({STATUS: SUCCESS, MESSAGE: levels})
