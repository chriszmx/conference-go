from django.http import JsonResponse
from common.json import ModelEncoder
from events.api_views import ConferenceListEncoder
from events.models import Conference
from .models import Attendee
from django.views.decorators.http import require_http_methods
import json


class ShowAttendeeListEncoder(ModelEncoder):
    model = Attendee
    properties = [
        "name"
    ]


@require_http_methods(["GET", "POST"])
def api_list_attendees(request, conference_id):
    if request.method == "GET":
        attendee = Attendee.objects.filter(conference=conference_id)
        return JsonResponse(
            {"attendee": attendee},
            encoder=ShowAttendeeListEncoder
        )
    else:
        content = json.loads(request.body)
        try:
            conference = Conference.objects.get(id=conference_id)
            content['conference'] = conference
        except Conference.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid conference id"},
                status=400,
            )
        attendee = Attendee.objects.create(**content)
        return JsonResponse(
            attendee,
            encoder=ShowAttendeeListEncoder,
            safe=False,
        )


class ShowAttendeeEncoder(ModelEncoder):
    model = Attendee
    properties = [
        "email",
        "name",
        "company_name",
        "created",
        "conference",
    ]
    encoders = {
        "conference": ConferenceListEncoder(),
    }


@require_http_methods(["DELETE", "GET", "PUT"])
def api_show_attendee(request, id):
    if request.method == 'GET':
        attendee = Attendee.objects.get(id=id)
        return JsonResponse(
            attendee,
            encoder=ShowAttendeeEncoder,
            safe=False,
        )
    elif request.method == "DELETE":
        count, _ = Attendee.objects.filter(id=id).delete()
        return JsonResponse(
            {"deleted": count > 0}
            )
    else:
        content = json.loads(request.body)
        try:
            conference = Conference.objects.get(name=content["conference"])
            content["conference"] = conference
        except Conference.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid attendee name"},
                status=400,
            )
        Attendee.objects.filter(id=id).update(**content)
        attendee = Attendee.objects.get(id=id)
        return JsonResponse(
            attendee,
            encoder=ShowAttendeeEncoder,
            safe=False,
        )
