from django.http import JsonResponse
from events.encoders import (ConferenceDetailEncoder,
                             ConferenceListEncoder,
                             LocationListEncoder,
                             LocationDetailEncoder)
from .models import Conference, Location
from django.views.decorators.http import require_http_methods
import json
from .models import State


def api_list_conferences(request):
    conferences = Conference.objects.all()
    return JsonResponse(
        {"conferences": conferences},
        encoder=ConferenceListEncoder,
    )


def api_show_conference(request, id):
    conference = Conference.objects.get(id=id)
    return JsonResponse(
        conference,
        encoder=ConferenceDetailEncoder,
        safe=False,
    )


@require_http_methods(["GET", "POST"])
def api_list_locations(request):
    if request.method == "GET":
        location = Location.objects.all()
        return JsonResponse(
            {"location": location},
            encoder=LocationListEncoder,
        )
    # handles POST
    else:
        content = json.loads(request.body)
        # get the state object and put it in the content dict
        try:
            state = State.objects.get(abbreviation=content["state"])
            content["state"] = state
        except State.DoesNotExist:
            return JsonResponse(
                {"message": 'Invalid state abbreviation'},
                status=400,
            )
        location = Location.objects.create(**content)
        return JsonResponse(
            location,
            encoder=LocationDetailEncoder,
            safe=False,
        )


@require_http_methods(["DELETE", "GET", "PUT"])
def api_show_location(request, id):
    if request.method == "GET":
        location = Location.objects.get(id=id)
        return JsonResponse(
            location,
            encoder=LocationDetailEncoder,
            safe=False,
        )
    elif request.method == "DELETE":
        count, _ = Location.objects.filter(id=id).delete()
        return JsonResponse(
            {"deleted": count > 0}
        )
    else:
        content = json.loads(request.body)
        try:
            if "state" in content:
                state = State.objects.get(abbreviation=content["state"])
                content["state"] = state
        except State.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid state abbreviation"},
                status=400,
            )
        Location.objects.filter(id=id).update(**content)
        location = Location.objects.get(id=id)
        return JsonResponse(
            location,
            encoder=LocationDetailEncoder,
            safe=False,
        )
