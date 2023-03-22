from django.http import JsonResponse
from .models import Presentation
from common.json import ModelEncoder


class PresentationListEncoder(ModelEncoder):
    model = Presentation
    properties = [
        "title",
    ]

    def get_extra_data(self, o):
        return {"status": o.status.name}


def api_list_presentations(request, conference_id):
    presentations = Presentation.objects.filter(conference=conference_id)
    return JsonResponse(
        {"presentations": presentations},
        encoder=PresentationListEncoder,
    )


class PresentationDetailEncoder(ModelEncoder):
    model = Presentation
    properties = [
        "presenter_name",
        "company_name",
        "presenter_email",
        "title",
        "synopsis",
        "created",
    ]


def api_show_presentation(request, id):
    presentation = Presentation.objects.get(id=id)
    return JsonResponse(
        presentation,
        encoder=PresentationDetailEncoder,
        safe=False,
    )
