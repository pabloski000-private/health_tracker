import json
import secrets
from datetime import date as date_type
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.utils.dateparse import parse_date

from .models import WeightEntry

# Create your views here.
@login_required
def calendar_view(request):
    return render(request, "any/calendar.html")

@login_required
def weights_json(request):
    entries = WeightEntry.objects.filter(user=request.user).order_by("date")
    events = [
        {"title": f"{e.weight} kg", "start": e.date.isoformat(), "allDay": True}
        for e in entries
    ]
    return JsonResponse(events, safe=False)

@login_required
def add_weight(request):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")

    d = parse_date(payload.get("date", ""))
    w = payload.get("weight", None)
    if not d or w is None:
        return HttpResponseBadRequest("Missing date/weight")

    WeightEntry.objects.update_or_create(
        user=request.user,
        date=d,
        defaults={"weight": w},
    )
    return JsonResponse({"ok": True})

@login_required
def weights_series(request):
    qs = WeightEntry.objects.filter(user=request.user).order_by("date").values("date", "weight")

    labels = [row["date"].isoformat() for row in qs]
    data = [float(row["weight"]) for row in qs]
    return JsonResponse({"labels": labels, "data": data})
