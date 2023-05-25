from django.shortcuts import render
from points.points import create_points_by_pic, connect_point_one_type, connect_point_other_types

def main_page(request):
    return render(request, "./index.html")

def floors_page(request):
    return render(request, "./floorsPage.html")

def create_page(request):
    return render(request, "./pathCreatePage.html")

