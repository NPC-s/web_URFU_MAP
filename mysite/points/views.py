from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from points.points import create_path, get_all_classrooms
from points.models import ClassRoom, Point
from django.core import serializers

def result_page(request : HttpRequest):
    start = Point.objects.get(id = int(request.POST["start_point"]))
    end = Point.objects.get(id = int(request.POST["end_point"]))
    return render(request, "./floorWithPath.html", {"path" : [a.as_json(False) for a in create_path(start, end)]})