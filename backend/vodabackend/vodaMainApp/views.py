"""
Views for VodaBackend.
"""
# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest
import random, array #temporary for dummy data
from .models import State, Sources, Contaminants, SourceLevels, State_Avg_Levels
import json

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

    # sorts the Sources model by states then by number_served in decending order. Only including
    # the first unique state
    largestSourceByState = Sources.objects.order_by('state', '-number_served').distinct('state')
    
    # makes the list of QuerySets into a list of State's and a list of cooresponding scores
    largestSourceByState = list(map(lambda qSet : list(qSet.state, qSet.score), largestSourceByState))
    #largestSourceScores = list(map(lambda qSet : qSet.score, largestSourceByState))

    data = {"data": largestSourceByState}
    json_data = json.dumps(data)
        
    return HttpResponse(json_data)


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
        searchedSource = SourceLevels.objects.filter(source_id = supply_id) #list of contaminants in that source
        contaminantIds = list(map(lambda qSet : qSet.contaminant_id, searchedSource))
        contaminantLevels = list(map(lambda qSet : qSet.contaminant_level, searchedSource))
        contaminantName = list(map(lambda qSet : Contaminants.objects.get(contaminant_id = qset), contaminantIds))
        data = {"Contaminant": contaminantName, "Level": contaminantLevels}
        #response = "Returns the summary details for water supply %s."
        #return HttpResponse(response % supply_id)
        json_data = json.dumps(data)

        return HttpResponse(json_data)
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

        response = "Returns the full details for water supply %s."
        return HttpResponse(response % supply_id)
    else:
        return HttpResponseBadRequest(400)


def debug(request):
    """ Debug endpoint.

    Returns the request object for easy debugging calls from the frontend.

    Args:
        request: Incoming Django request object.

    Returns:
        An HTTP Response with details from the request object.
    """
    return HttpResponse(("Request received: ",
                         "host: %s, " % request.get_host(),
                         "type: %s, " % request.method,
                         "GET params: " + str(request.GET) + ", ",
                         "POST params: " + str(request.POST)))
