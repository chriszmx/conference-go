from django.http import JsonResponse
from common.json import ModelEncoder
from events.api_views import ConferenceListEncoder
from .models import Attendee


class ShowAttendeeListEncoder(ModelEncoder):
    model = Attendee
    properties = [
        "name"
    ]


def api_list_attendees(request, conference_id):
    attendee = Attendee.objects.filter(conference=conference_id)
    return JsonResponse(
        {"attendee": attendee},
        encoder=ShowAttendeeListEncoder
    )


class ShowAttendeeEncoder(ModelEncoder):
    model = Attendee
    properties = [
        "email",
        "name",
        "company_name",
        "created",
    ]
    encoders = {
        "conference": ConferenceListEncoder(),
    }


def api_show_attendee(request, id):
    attendee = Attendee.objects.get(id=id)
    return JsonResponse(
        attendee,
        encoder=ShowAttendeeEncoder,
        safe=False,
    )
