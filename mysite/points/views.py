from django.shortcuts import render
from points.models import Points

def result_page(requset):
    start = requset.POST["start_point"]
    end = requset.POST["end_point"]
    start_point = Points.objects.filter(id = int(start))[0]
    end_point = Points.objects.filter(id = int(end))[0]
    return render(requset, "./result_page.html", {"path" : create_path(start_point, end_point)})

def create_path(start : Points, end : Points) -> list | None:
    if start.type == Points.PointType.classroom and end.type == Points.PointType.classroom:
        pass
    #TODO : rewrite realization of creating path
