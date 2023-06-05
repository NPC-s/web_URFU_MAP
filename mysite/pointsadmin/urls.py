from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='admin_index'),
    path('pointschangename', views.rename_page, name='admin_remane_point_name'),
    path('loadnewmap', views.load_map, name='admin_load_map'),
]