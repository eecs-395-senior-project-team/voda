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

    # sorts the Sources model by County then by number_served in decending order. Only including
    # the first unique County
    largest_source_by_county = Sources.objects.order_by('county', '-number_served').distinct('county')

    largest_source_by_county = list(
        map(
            lambda qSet: list(qSet.county, qSet.county),
        largest_source_by_county))
    largest_source_scores = list(
        map(
            lambda qSet: qSet.score, largest_source_by_county))

    response_data = list(
        map(
            lambda county, score: {
                'county': county,
                'score': score,
            },
            largest_source_by_county, largest_source_scores))

    response = {
        "sources": response_data
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

    # going to be formated as
    # if there are no contaminants over the recomended amount
    # All contaminants are below the health guideline set by the California Office of Environmental Health Hazard Assessment.

    # <number of contaminants over recomended> contaminants were found in the water from the <source name> source.
    # They are as follows <list of contaminant names over the regulated amount


    supply_id = request.GET.get('source')
   
    if supply_id:
        #searchedSource = SourceLevels.objects.filter(source_id = supply_id) #list of contaminants in that source
        #contaminantIds = list(map(lambda qSet : qSet.contaminant_id, searchedSource))
        #contaminantLevels = list(map(lambda qSet : qSet.contaminant_level, searchedSource))
        #presentContaminants = map(lambda qSet : Contaminants.objects.get(contaminant_id = qSet, contaminantIds))
        #data = map(lambda presentContaminants, contaminantLevels: list(presentContaminants.contaminant_name, presentContaminants.health_guideline, contaminantLevels))
        #filteredData = filter(lambda dataToFilter : dataToFilter[1] > dataToFilter[2], data) #filter out contaminants that aren't past the health guideline
        #numberOfHighContams = len(filteredData)
        #filteredData = map(lambda data : data[0], filteredData)
        #filteredData = ','.join(filteredData)

        #if numberOfHighContams == 0:
        #    response = "All contaminants are below the health guideline set by the California Office of Environmental Health Hazard Assessment."
        #    return HttpResponse(response)
        #else:
        #    response = "%s contaminants were found in the water from the <source name> source. They are as follows " + filteredData
        #    return HttpResponse(response % numberOfHighContams)#/


        # if present contaminant regulated level > 

        response = "Returns the summary details for water supply %s."
        return HttpResponse(response % supply_id)

        # test version        
        #searchedSource = SourceLevels.objects.filter(source_id = supply_id)
        #data = {"Level": contaminantLevels}
        #json_data = json.dumps(data)

        #return HttpResponse(json_data)
    else:
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

    # details will be formated as a list of all of the contaminants that are above regulation it will have the following information

    # The following contaminants in <source name> were over the maximum amount in parts per billion 
    #recomended by the California Office of Environmental Health Hazard Assessment.

    # <Name Of Contaminant>
    # Level in water <contaminant_level>
    # Level recomented <health_guideline>
    # Legal limit <legal limit>
    # High levels of <Name of contaminant> can lead to.
    # <Health Concerns>

    supply_id = request.GET.get('source')

    if supply_id:
        #searchedSource = SourcesLevels.objects.filter(source_id = supply_id) #list of contaminants in that source
        #contaminantIds = map(lambda qSet : qSet.contaminant_id, searchedSource)

        #searchedSource = SourceLevels.objects.filter(source_id = supply_id) #list of contaminants in that source
        #contaminantIds = list(map(lambda qSet : qSet.contaminant_id, searchedSource))
        #presentContaminants = map(lambda qSet : Contaminants.objects.get(contaminant_id = qSet, contaminantIds))
        #contaminantLevels = list(map(lambda qSet : qSet.contaminant_level, searchedSource))

        #responseString = "The following contaminants in <source name> were over the maximum amount in parts per billion recomended by the California Office of Environmental Health Hazard Assessment. \n\n"
        #responseString += list(map(formatContamDetails, presentContaminants, contaminantLevels))

        #def formatContamDetails(contaminant, contaminantLevels):
        #    contaminantName = contaminant.contaminant_name
        #    response = contaminant.contaminant_name + ":\n"
        #    response += contaminantName + " levels found in water: " + contaminantLevels + "\n"
        #    response += "Recomended level of " + contaminantName + ": " + contaminant.health_guideline + "\n"
        #    response += "Legal limit of " + contaminantName + ": " + contaminant.legal_limit + "\n"
        #    response += "High levels of " + contaminantName + " can lead to:\n"
        #    response += contaminant.health_concerns + "\n"

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
