from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest

"""
Returns a list of water supplies and a 1-10 value with the quality of the water. 
This is called by the frontend every time it is loaded to allow the map to be colored. 
The frontend will convert the 1-10 value to red-green gradient value.

:param request
:type Http request
:return list of water supply int pairs
"""
def map(request):
    return HttpResponse("Returns a list of water supplies and a 1-10 value with the quality of the water.")

"""
Returns the summary details for the given water supply. Called by the frontend when a user clicks on water supply.

:param request
:type Http request
:return String
"""
def summary(request):

    #error Check
    supply_id = request.GET.get('source')
    
    if supply_id:
        response = "Returns the summary details for water supply %s."
        return HttpResponse(response % supply_id)
    else:
        return HttpResponseBadRequest(400)

"""
Returns the full details for a given water supply. Called by the frontend when a user clicks on the more details link from the card view.
Called from .../vodaMainApp/urls.py

:param request
:type Http request
: return String
"""

def details(request):
    #error check
    supply_id = request.GET.get('source')
    #error check

    if supply_id:
        response = "Returns the full details for water supply %s."
        return HttpResponse(response % supply_id)
    else:
        return HttpResponseBadRequest(400)


