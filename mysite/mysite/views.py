from django.shortcuts import render
from enums import INSTITUES

from points.models import MapImages, Point
from points.points import get_classroom


def main_page(request):
    return render(request, "./index.html")

def floors_page(request):
    return render(request, "./floorsPage.html")

def floor_page(request, institue : INSTITUES, floor : int):
    image_data = MapImages.objects.get(institue = institue, floor = floor)
    return render(request, "./floor.html", {"image_path" : image_data.image.name[7:] })

def create_page(request):
    points = Point.objects.filter(type__in = [3, 5])
    points_json = [p.as_json() for p in points]
    for p_json in points_json:
        classroom = get_classroom(int(p_json['pk']))
        if classroom:
            p_json['name'] = classroom.number_of_class
        else:
            p_json["name"] = "Вход"
    return render(request, "./pathCreatePage.html", {"classrooms" : points_json})
