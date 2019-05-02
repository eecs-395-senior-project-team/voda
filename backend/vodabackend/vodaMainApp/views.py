"""
Views for VodaBackend.
"""
# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from .models import Sources, SourceLevels


def root(request):
    """ Root endpoint.

    Base url to announce that the server is running. More of a sanity check than anything.

    Args:
        request: Incoming Django request object.

    Returns:
        An HTTP Response announcing that the server is alive.
    """
    return HttpResponse("Server Alive.")


def map_endpoint(request):
    """ Map endpoint

    Returns a list of water supplies and a 1-10 value with the quality of the water.
    The frontend will convert the 1-10 value to red-green gradient value.
    Named map_endpoint to avoid overwritting builtin map.

    Args:
        request: Incoming Django request object.

    Returns:
        An HTTP Response with a list of water supplies and their associated 1-10 values.
    """
    largest_source_by_county = Sources.objects.order_by('county', '-number_served').distinct('county')
    scores = {}
    source_ids = {}
    for q_set in largest_source_by_county:
        scores[q_set.county.id] = q_set.rating
        source_ids[q_set.county.id] = q_set.source_id
    response = {
        "scores": scores,
        "sourceIDs": source_ids
    }
    print(response)
    return JsonResponse(response)


def summary(request):
    """ Summary endpoint

    Returns the summary details for the given water supply.

    Args:
        request: Incoming Django request object.

    Returns:
        An HTTP Response with the summary for the requested water supply.
        or
        An HTTPResponseBadRequest if the 'source' param is missing.
    """
    supply_id = request.GET.get('source')
    try:
        source = Sources.objects.get(source_id=supply_id)
        source_levels = source.sourcelevels_set.all()
        red_set = []
        yellow_set = []
        green_set = []
        for source_level in source_levels:
            contaminant = source_level.contaminant
            if source_level.contaminant_level > contaminant.legal_limit:
                red_set.append(contaminant)
            if source_level.contaminant_level > contaminant.health_guideline:
                yellow_set.append(contaminant)
            if source_level.contaminant <= contaminant.health_guideline and source_level.contaminant <= contaminant.legal_limit:
                green_set.append(contaminant)
        response = {
            "legalLimitConcerns": ['a', 'b', 'c', 'd', 'e'],
            "healthGuidelinesConcerns": ['a', 'b', 'c', 'd', 'e', 'f'],
            "redCount": len(red_set),
            "yellowCount": len(yellow_set),
            "greenCount": len(green_set),
        }
        return JsonResponse(response)
    except:
        return HttpResponseBadRequest(400)


def contaminants(request):
    supply_id = request.GET.get('source')
    try:
        source = Sources.objects.get(source_id=supply_id)
        source_levels = source.sourcelevels_set.all()
        red_set = []
        yellow_set = []
        green_set = []
        for source_level in source_levels:
            contaminant = source_level.contaminant
            if source_level.contaminant_level > contaminant.legal_limit:
                red_set.append(contaminant.contaminant_name)
            if source_level.contaminant_level > contaminant.health_guideline:
                yellow_set.append(contaminant.contaminant_name)
            if source_level.contaminant <= contaminant.health_guideline and source_level.contaminant <= contaminant.legal_limit:
                green_set.append(contaminant.contaminant_name)
        contaminant_list = {
            "redContaminants": red_set,
            "yellowContaminants": yellow_set,
            "greenContaminants": green_set
        }
        return JsonResponse(contaminant_list)
    except:
        return HttpResponseBadRequest(400)


def contaminant_info(request):
    supply_id = request.GET.get('source')
    contaminant_name = request.GET.get('contaminant')
    if True:
    #if supply_id and contaminant_name:
        contaminant_details = {
            "Amount in water": 7.38,
            "Health Guideline": 0.06,
            "Legal Limit": 999.99,
            "Details": "Bromodchloromecahne, one of the total TTHMs, is formed when chlorine or other disinfectants are used to treat drinking water. Bromodchloromecahne and other disinfection byproducts inrease the risk of cancer and may cause problems during pregnancy."
        }
        return JsonResponse(contaminant_details)
    return HttpResponseBadRequest(400)


def debug(request):
    """ Debug endpoint.

    Returns the request object for easy debugging calls from the frontend.

    Args:
        request: Incoming Django request object.

    Returns:
        A JsonResponse with details from the request object.
    """
    response = {
        "Request Received":
            {
                "Host": request.get_host(),
                "Type": request.method,
                "GET Params": request.GET,
                "POST Params": request.POST,
            }
    }
    return JsonResponse(response)
