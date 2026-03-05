import json
import secrets
from datetime import date as date_type
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.utils.dateparse import parse_date

from .models import WeightEntry

# Create your views here.
def get_client_id(request) -> str:
    # Requires Django sessions middleware (default in new projects)
    cid = request.session.get("client_id")
    if not cid:
        cid = secrets.token_hex(16)  # 32 hex chars
        request.session["client_id"] = cid
    return cid

def calendar_view(request):
    return render(request, "any/calendar.html")

def weights_json(request):
    cid = get_client_id(request)
    entries = WeightEntry.objects.filter(client_id=cid).order_by("date")
    events = [
        {"title": f"{e.weight} kg", "start": e.date.isoformat(), "allDay": True}
        for e in entries
    ]
    return JsonResponse(events, safe=False)


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

    cid = get_client_id(request)
    WeightEntry.objects.update_or_create(
        client_id=cid,
        date=d,
        defaults={"weight": w},
    )
    return JsonResponse({"ok": True})

def weights_series(request):
    cid = get_client_id(request)  # the same session-based function you already use
    qs = WeightEntry.objects.filter(client_id=cid).order_by("date").values("date", "weight")

    labels = [row["date"].isoformat() for row in qs]
    data = [float(row["weight"]) for row in qs]
    return JsonResponse({"labels": labels, "data": data})
