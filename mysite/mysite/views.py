from django.shortcuts import render
from enums import INSTITUES
from points.models import MapImages

def main_page(request):
    return render(request, "./index.html")

def floors_page(request):
    return render(request, "./floorsPage.html")

def floor_page(request, institue : INSTITUES, floor : int):
    image_data = MapImages.objects.get(institue = institue, floor = floor)
    return render(request, "./floor.html", {"image_path" : image_data.image.name[7:] })

def create_page(request):
    return render(request, "./pathCreatePage.html")

