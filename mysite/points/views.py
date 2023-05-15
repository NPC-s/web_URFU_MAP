from django.shortcuts import render
from points.points import create_path
from points.models import Point

def result_page(requset):
    start = Point.objects.get(id = int(requset.POST["start_point"]))
    end = Point.objects.get(id = int(requset.POST["end_point"]))
    return render(requset, "./result_page.html", {"path" : create_path(start, end)})