import datetime

from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from schedule.models import Slot, Presentation


wed_morn_start = datetime.datetime(2011, 3, 9, 9, 0)  # 9AM Eastern
wed_morn_end = datetime.datetime(2011, 3, 9, 12, 20)  # 12:20PM Eastern
wed_after_start = datetime.datetime(2011, 3, 9, 14, 0)  # 2PM Eastern
wed_after_end = datetime.datetime(2011, 3, 9, 16, 40)  # 4:40PM Eastern
thu_morn_start = datetime.datetime(2011, 3, 10, 9, 0)  # 9AM Eastern
thu_morn_end = datetime.datetime(2011, 3, 10, 12, 20)  # 12:20PM Eastern
thu_after_start = datetime.datetime(2011, 3, 10, 14, 0)  # 2PM Eastern
thu_after_end = datetime.datetime(2011, 3, 10, 16, 40)  # 4:40PM Eastern

WEDNESDAY_MORNING = (wed_morn_start, wed_morn_end)
WEDNESDAY_AFTERNOON = (wed_after_start, wed_after_end)
THURSDAY_MORNING = (thu_morn_start, thu_morn_end)
THURSDAY_AFTERNOON = (thu_after_start, thu_after_end)


def schedule_list(request, template_name="schedule/schedule_list.html", extra_context=None):
    
    if extra_context is None:
        extra_context = {}
    
    slots = Slot.objects.all().order_by("start")
    
    return render_to_response(template_name, dict({
        "slots": slots,
        "timezone": settings.SCHEDULE_TIMEZONE,
    }, **extra_context), context_instance=RequestContext(request))


def schedule_presentation(request, presentation_id, template_name="schedule/presentation_detail.html", extra_context=None):
    
    if extra_context is None:
        extra_context = {}
    
    presentation = get_object_or_404(Presentation, id=presentation_id)
    
    return render_to_response(template_name, dict({
        "presentation": presentation,
        "timezone": settings.SCHEDULE_TIMEZONE,
    }, **extra_context), context_instance=RequestContext(request))


def schedule_list_talks(request):
    
    talks = Presentation.objects.filter(
        presentation_type__in=[Presentation.PRESENTATION_TYPE_PANEL, Presentation.PRESENTATION_TYPE_TALK]
    )
    talks = talks.order_by("pk")
    
    return render_to_response("schedule/list_talks.html", dict({
        "talks": talks,
    }), context_instance=RequestContext(request))


def schedule_list_tutorials(request):
    
    tutorials = Presentation.objects.filter(
        presentation_type=Presentation.PRESENTATION_TYPE_TUTORIAL
    )
    tutorials = tutorials.order_by("pk")
    
    return render_to_response("schedule/list_tutorials.html", dict({
        "tutorials": tutorials,
    }), context_instance=RequestContext(request))


def schedule_list_posters(request):
    
    posters = Presentation.objects.filter(
        presentation_type=Presentation.PRESENTATION_TYPE_POSTER
    )
    posters = posters.order_by("pk")
    
    return render_to_response("schedule/list_posters.html", dict({
        "posters": posters,
    }), context_instance=RequestContext(request))


def schedule_tutorials(request):
    
    tutorials = {
        "wed": {
            "morning": {
                "slot": WEDNESDAY_MORNING,
                "presentations": Presentation.objects.filter(
                    slot__start=WEDNESDAY_MORNING[0]
                ).order_by("pk"),
            },
            "afternoon": {
                "slot": WEDNESDAY_AFTERNOON,
                "presentations": Presentation.objects.filter(
                    slot__start=WEDNESDAY_AFTERNOON[0]
                ).order_by("pk"),
            }
        },
        "thurs": {
            "morning": {
                "slot": THURSDAY_MORNING,
                "presentations": Presentation.objects.filter(
                    slot__start=THURSDAY_MORNING[0]
                ).order_by("pk"),
            },
            "afternoon": {
                "slot": THURSDAY_AFTERNOON,
                "presentations": Presentation.objects.filter(
                    slot__start=THURSDAY_AFTERNOON[0]
                ).order_by("pk"),
            }
        }
    }
    
    ctx = {
        "tutorials": tutorials,
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("schedule/tutorials.html", ctx)
