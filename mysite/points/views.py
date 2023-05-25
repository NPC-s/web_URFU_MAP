from django.shortcuts import render
from points.points import create_path
from points.models import Point
from django.core import serializers

def result_page(request):
    start = Point.objects.get(id = int(request.POST["start_point"]))
    end = Point.objects.get(id = int(request.POST["end_point"]))
    return render(request, "./floorWithPath.html", {"path" : serializers.serialize("json", create_path(start, end))})