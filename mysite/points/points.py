from __future__ import annotations
from points.models import Point
import queue
from points.models import Point, Path, ClassRoom, PointType
from django.db.models import Q
from typing import Literal

_INSTITUES = Literal["RI"]

"""def create_path_from_many(start_point_id : int, end_point_id : int) -> list | None:
    start = Points.objects.get(id = int(start_point_id))
    end = Points.objects.get(id = int(end_point_id))
    print(start.institue, end.institue, start.institue==end.institue)
    result = []
    if start.type == PointType.classroom and end.type == PointType.classroom:
        try:
            raise
            path_raw = Pathes.objects.get(start_point_id = start_point_id, end_point_id = end_point_id)
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

                return path_to_door_from_start.path.extend(
                    path_between_inst.path).extend( # type: ignore
                    path_to_door_from_end.path.reverse())

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
                raw_points = raw_points.filter(floor = start.floor,
                                                relativeX__range = (min(start.relativeX, end.relativeX), max(start.relativeX, end.relativeX)),
                                                relativeY__range = (min(start.relativeY, end.relativeY), max(start.relativeY, end.relativeY)))
                

            print(raw_points.values_list("id", "institue", "type", "relativeX", "relativeY", "connections", "floor"))

            for point in raw_points.values_list("id", "institue", "type", "relativeX", "relativeY", "connections", "floor"):
                new_point = Point(point.id) #Нужны реальные данные, чтобы точнее можно было понять сортировку

                #TODO : Create appending points to graph, after inserting real data"""
            
class SinglyLinkedList():
    def __init__(self, point : Point, prev : SinglyLinkedList | None) -> None:
        self.point = point
        self.prev = prev

def create_path(start : Point, end : Point):
    visitedIds : set[int] = set()

    ways : queue.Queue[SinglyLinkedList] = queue.Queue()
    ways.put(SinglyLinkedList(start, None))

    shortestWay = None

    while not ways.empty():
        way = ways.get()

        for id in way.point.conns['conns']:
            if id in visitedIds:
                continue
            visitedIds.add(id)
            newPoint = Point.objects.get(id = id)
            newWay = SinglyLinkedList(newPoint, way)
            ways.put(newWay)
            if id == end.id:
                shortestWay = newWay
                break
    
    result = []
    if shortestWay is not None:
        
        while shortestWay.prev is not None:
            result.append(shortestWay.point)
            shortestWay = shortestWay.prev

        result.append(start)

        result.reverse()

    print(result)
    return result

def create_points_by_pic(dir : str, institue : str, floor : int):
    from PIL import Image
    img = Image.open(dir)
    for x in range(1, img.width):
        for y in range(1, img.height):
            r, g, b, a = img.getpixel((x, y))
            hex_code = '#{:02x}{:02x}{:02x}'.format(r, g, b)
            match hex_code:
                case "#23234214134":
                    add_point_to_model(x, y, 0, institue, floor)
                case "#2400ff":
                    add_point_to_model(x, y, 1, institue, floor)
                case "#fa05f0":
                    add_point_to_model(x, y, 2, institue, floor)
                case "#00ffff":
                    add_point_to_model(x, y, 3, institue, floor)
                case "#00ff00":
                    add_point_to_model(x, y, 4, institue, floor)
                case "#23234214134":
                    add_point_to_model(x, y, 5, institue, floor)

def add_point_to_model(x : int, y : int, type : int, institue : str, floor : int):
    try:
        Point.objects.get(x = x, y = y, type = type, institue = institue, floor = floor)
    except:
        new_point = Point(type = type,
                        institue = institue,
                        relativeX = x,
                        relativeY = y,
                        floor = floor)
        new_point.save()
        if type == 3:
            new_classroom = ClassRoom(number_of_class = "N/A", id_of_point = new_point.id)
            new_classroom.save()

def connect_point_other_types(start_type : int, end_type : int, institue : _INSTITUES, floor : int):
    start_points = Point.objects.filter(type = start_type, institue = institue, floor = floor)
    for classroom in start_points:
        end_points = Point.objects.filter(relativeX = classroom.relativeX, type = end_type, institue = institue, floor = floor)
        searching_by = "X"
        if len(end_points) == 0:
            end_points = Point.objects.filter(relativeY = classroom.relativeY, type = end_type, institue = institue, floor = floor)
            searching_by = "Y"
            if len(start_points) == 0:
                print(classroom, "не нашел совпадений")

        if len(end_points) == 1:
            classroom.connect(end_points[0])
        
        else:
            if searching_by == "X":
                sorted_preclassrooms = sorted(end_points, key = lambda precl : abs(precl.relativeX - classroom.relativeX))
            else:
                sorted_preclassrooms = sorted(end_points, key = lambda precl : abs(precl.relativeY - classroom.relativeY))

            classroom.connect(sorted_preclassrooms[0])

def connect_point_one_type(type : int, institue : _INSTITUES, floor : int):
    points = Point.objects.filter(type = type, institue = institue, floor = floor)
    for point in points:
        for point2 in points:
            if point.relativeX == point2.relativeX or point.relativeY == point2.relativeY:
                point.connect(point2)