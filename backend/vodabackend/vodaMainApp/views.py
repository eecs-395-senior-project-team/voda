"""
Views for VodaBackend.
"""
# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from .models import Sources


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
    #TODO: Change to FIPS code
    sources = {}
    for q_set in largest_source_by_county:
        sources[q_set.county] = q_set.score
    return JsonResponse(sources)


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
    if supply_id:
        response = {
            "legalLimitConcerns": ['a', 'b', 'c', 'd', 'e'],
            "healthGuidelinesConcerns": ['a', 'b', 'c', 'd', 'e', 'f'],
            "redCount": 3,
            "yellowCount": 8,
            "greenCount": 215,
        }
        return JsonResponse(response)
    return HttpResponseBadRequest(400)


def details(request):
    """ Details endpoint.

    Returns the full details for a given water supply.
    Called by the frontend when a user clicks on the more details link from the card view.

    Args:
        request: Incoming Django request object.

    Returns:
        An HTTP Response with the details for the requested water supply.

        or

        An HTTPResponseBadRequest if the 'source' param is missing.
    """
    supply_id = request.GET.get('source')
    if supply_id:
        response_string = "This is a test String"
        return HttpResponse(response_string)
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
