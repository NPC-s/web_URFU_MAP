import os

from django.core.files.storage import default_storage
from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect

from points.forms import MapImageForm
from points.models import ClassRoom, MapImages, Point
from points.points import get_all_classrooms

from .forms import MapImageEditForm
from .points_admin import *

def index(request : HttpRequest):
    if not request.user.is_superuser: # type: ignore
        return HttpResponseRedirect("/")
    return render(request, "./Admin/MainPage.html")

def rename_page(request : HttpRequest, institue : INSTITUES, floor : int):
    if not request.user.is_superuser: # type: ignore
        return HttpResponseRedirect("/")
    image_data = MapImages.objects.get(institue = institue, floor = floor)
    if request.method == "POST":
        class_room = ClassRoom.objects.get(id_of_point = int(request.POST["id_of_point"]))
        new_name = request.POST["number_of_class"]
        class_room.number_of_class = "N/A" if new_name == '' else new_name
        class_room.save()
    return render(request, "./Admin/RenamePoints.html", {"points" : get_all_classrooms(institue, floor),
                                                         "image_path" : image_data.image.name[7:],
                                                         "floor" : floor,
                                                         "institue" : institue,
                                                         "all_points" : [p.as_json() for p in Point.objects.filter(institue = institue, floor = floor)]})

def load_map(request : HttpRequest):
    if not request.user.is_superuser: # type: ignore
        return HttpResponseRedirect("/")
    form_load = MapImageForm()
    form_edit = MapImageEditForm()

    if request.method == 'POST':
        if "image" in request.FILES:
            form_load = MapImageForm(request.POST, request.FILES)
            if form_load.is_valid():
                form_load.save()
        
        if "do" in request.POST:
            form_edit = MapImageEditForm(request.POST)
            if form_edit.is_valid():
                image = MapImages.objects.get(pk=request.POST['pk'])
                if request.POST['do'] == 'update':
                    image.institue = request.POST['institue']
                    image.floor = int(request.POST['floor'])
                    image.save()
                elif request.POST['do'] == 'delete':
                    file_path = image.image.path
                    image.delete()
                    delete_point(request.POST['institue'], int(request.POST['floor']))
                    os.remove(file_path)
                elif request.POST['do'] == "create_points":
                    create_points_by_pic(image.image.path, image.institue, image.floor)
                    connect_point_one_type(1, image.institue, image.floor)
                    connect_point_one_type(2, image.institue, image.floor)
                    connect_point_other_types(3, 2, image.institue, image.floor)
                    connect_point_other_types(4, 2, image.institue, image.floor)
                    connect_point_other_types(2, 1, image.institue, image.floor)
                    connect_point_other_types(4, 1, image.institue, image.floor)
                    connect_point_other_types(5, 1, image.institue, image.floor)
                    connect_point_other_types(5, 2, image.institue, image.floor)

    images = MapImages.objects.all()
    return render(request, './Admin/UploadImage.html', {'form_load': form_load, "form_edit" : form_edit, "images" : images})
