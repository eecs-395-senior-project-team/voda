from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def map(request):
    return HttpResponse("Returns a list of water supplies and a 1-10 value with the quality of the water.")

def summary(request, supply_id):
    response = "Returns the summary details for water supply %s."
    return HttpResponse(response % supply_id)

def details(request, supply_id):
    return HttpResponse("Returns the full details for water supply %s." % supply_id)


