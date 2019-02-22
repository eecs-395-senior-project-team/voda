from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest


def map(request):
    return HttpResponse("Returns a list of water supplies and a 1-10 value with the quality of the water.")

def summary(request):

    #error Check
    supply_id = request.GET.get('source')
    
    if supply_id:
        response = "Returns the summary details for water supply %s."
        return HttpResponse(response % supply_id)
    else:
        return HttpResponseBadRequest(400)





def details(request):
    #error check
    supply_id = request.GET.get('source')
    #error check

    if supply_id:
        response = "Returns the full details for water supply %s."
        return HttpResponse(response % supply_id)
    else:
        return HttpResponseBadRequest(400)

