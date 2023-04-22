from django.shortcuts import render
from django.db.models import Q
from points.models import Points, Pathes
from points.points import Graph, Point, find_path

def result_page(requset):
    start = requset.POST["start_point"]
    end = requset.POST["end_point"]
    return render(requset, "./result_page.html", {"path" : create_path(start, end)})

def create_path(start_point_id : int, end_point_id : int) -> list | None:
    start = Points.objects.filter(id = int(start_point_id))[0]
    end = Points.objects.filter(id = int(end_point_id))[0]
    result = []
    if start.type == Points.PointType.classroom and end.type == Points.PointType.classroom:
        path_raw = Pathes.objects.get(start_point_id = start_point_id, end_point_id = end_point_id)
        try:
            return path_raw.path
        except:
            graph = Graph()
            raw_points = Points.objects
            if start.institue != end.institue:
                try:
                    door_point_start_ints = Points.objects.get(institue = start.institue, type = "5")
                    path_to_door_from_start = Pathes.objects.get(start_point_id = start_point_id, end_point_id = door_point_start_ints)

                    door_point_end_ints = Points.objects.get(institue = end.institue, type = "5")
                    path_to_door_from_end = Pathes.objects.get(start_point_id = end_point_id, end_point_id = door_point_end_ints)

                    path_between_inst = Pathes.objects.get(start_point_id = door_point_start_ints, end_point_id = door_point_end_ints)

                    return path_to_door_from_start.path["connections"].extend(
                        path_between_inst.path["connections"]).extend(
                        path_to_door_from_end.path["connections"].reverse())

                except:

                    raw_points = raw_points.filter(Q(floor = start.floor, institue = start.institue)
                                                    | Q(floor = end.floor, institue = end.institue)
                                                    | Q(type = "4", institue = end.institue) | Q(type = "4", institue = end.institue)
                                                    | Q(type = "0"))
            else:
                if start.floor != end.floor:
                    raw_points = raw_points.filter(Q(floor__range = (min(start.floor, end.floor), max(start.floor, end.floor))) 
                                                    | Q(type = "4"))
                    
                else:
                    raw_points = raw_points.filter(floor__range = start.floor,
                                                    relativeX__range = (min(start.relativeX, end.relativeX), max(start.relativeX, end.relativeX)),
                                                    relativeY__range = (min(start.relativeY, end.relativeY), max(start.relativeY, end.relativeY)))
                
                for point in raw_points.values_list("id"):
                    new_point = Point(point.id) #Нужны реальные данные, чтобы точнее можно было понять сортировку

                    #TODO : Create appending points to graph, after inserting real data
            