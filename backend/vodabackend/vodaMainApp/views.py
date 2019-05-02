"""
Views for VodaBackend.
"""
# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from .models import Sources, SourceLevels
import traceback


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
            if source_level.contaminant_level:
                contaminant = source_level.contaminant
                if contaminant.legal_limit:
                    if source_level.contaminant_level > contaminant.legal_limit:
                        red_set.append(contaminant)
                if contaminant.health_guideline:
                    if source_level.contaminant_level > contaminant.health_guideline:
                        yellow_set.append(contaminant)
                if contaminant.legal_limit and contaminant.health_guideline:
                    if source_level.contaminant_level <= contaminant.health_guideline and source_level.contaminant_level <= contaminant.legal_limit:
                        green_set.append(contaminant)
        legal_limit_concerns = set()
        for contaminant in red_set:
            if contaminant.health_concerns:
                for concern in contaminant.health_concerns.splitlines():
                    formatted_concern = concern.strip().capitalize()
                    if formatted_concern not in legal_limit_concerns and formatted_concern != "":
                        legal_limit_concerns.add(formatted_concern)
        health_guidelines_concerns = set()
        for contaminant in yellow_set:
            if contaminant.health_concerns:
                for concern in contaminant.health_concerns.splitlines():
                    formatted_concern = concern.strip().capitalize()
                    if formatted_concern not in health_guidelines_concerns and formatted_concern != "":
                        health_guidelines_concerns.add(formatted_concern)
        response = {
            "legalLimitConcerns": list(legal_limit_concerns),
            "healthGuidelinesConcerns": list(health_guidelines_concerns),
            "redCount": len(red_set),
            "yellowCount": len(yellow_set),
            "greenCount": len(green_set),
        }
        return JsonResponse(response)
    except Exception as e:
        traceback.print_exc()
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
            if source_level.contaminant_level:
                contaminant = source_level.contaminant
                if contaminant.legal_limit:
                    if source_level.contaminant_level > contaminant.legal_limit:
                        red_set.append(contaminant.contaminant_name)
                if contaminant.health_guideline:
                    if source_level.contaminant_level > contaminant.health_guideline:
                        yellow_set.append(contaminant.contaminant_name)
                if contaminant.legal_limit and contaminant.health_guideline:
                    if source_level.contaminant_level <= contaminant.health_guideline and source_level.contaminant_level <= contaminant.legal_limit:
                        green_set.append(contaminant.contaminant_name)
        contaminant_list = {
            "redContaminants": red_set,
            "yellowContaminants": yellow_set,
            "greenContaminants": green_set
        }
        return JsonResponse(contaminant_list)
    except Exception:
        traceback.print_exc()
        return HttpResponseBadRequest(400)


def contaminant_info(request):
    supply_id = request.GET.get('source')
    contaminant_name = request.GET.get('contaminant')
    try:
        source_level = SourceLevels.objects \
                        .filter(source=supply_id) \
                        .get(contaminant__contaminant_name=contaminant_name)
        amount_in_water = round(float(source_level.contaminant_level), 2) if source_level.contaminant_level else None
        health_guideline = round(float(source_level.contaminant.health_guideline), 2) if source_level.contaminant.health_guideline else None
        legal_limit = round(float(source_level.contaminant.legal_limit), 2) if source_level.contaminant.legal_limit else None
        details = source_level.contaminant.summary.strip() if source_level.contaminant.summary else None
        health_risks = source_level.contaminant.long_health_concerns.strip if source_level.contaminant.long_health_concerns else None
        contaminant_details = {
            "Amount in water": amount_in_water,
            "Health Guideline": health_guideline,
            "Legal Limit": legal_limit,
            "Details": details,
            "Health Risks": health_risks
        }
        return JsonResponse(contaminant_details)
    except Exception as e:
        traceback.print_exc()
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
