from common.json import ModelEncoder
from events.models import Conference, Location


class ConferenceListEncoder(ModelEncoder):
    model = Conference
    properties = [
        "name",
    ]


class LocationListEncoder(ModelEncoder):
    model = Location
    properties = [
        "name",
    ]


class LocationDetailEncoder(ModelEncoder):
    model = Location
    properties = [
        "name",
        "city",
        "room_count",
        "created",
        "updated",
    ]

    def get_extra_data(self, o):
        return {"state": o.state.abbreviation}


class ConferenceDetailEncoder(ModelEncoder):
    model = Conference
    properties = [
        "name",
        "description",
        "max_presentations",
        "max_attendees",
        "starts",
        "ends",
        "created",
        "updated",
        "location",
    ]
    encoders = {
        "location": LocationListEncoder(),
    }
