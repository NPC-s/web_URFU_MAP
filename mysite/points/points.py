from __future__ import annotations
from points.models import Point
import queue
from points.models import Point, ClassRoom
from enums import INSTITUES
from dataclasses import dataclass, field
import math



# def create_path_from_many(start_point_id : int, end_point_id : int) -> list | None:
#     start = Points.objects.get(id = int(start_point_id))
#     end = Points.objects.get(id = int(end_point_id))
#     print(start.institue, end.institue, start.institue==end.institue)
#     result = []
#     if start.type == PointType.classroom and end.type == PointType.classroom:
#         try:
#             path_raw = Pathes.objects.get(start_point_id = start_point_id, end_point_id = end_point_id)
#             return path_raw.path
#         except:
#         graph = Graph()
#         raw_points = Points.objects
#         if start.institue != end.institue:
#             try:
#                 door_point_start_ints = Points.objects.get(institue = start.institue, type = "5")
#                 path_to_door_from_start = Pathes.objects.get(start_point_id = start_point_id, end_point_id = door_point_start_ints)

#                 door_point_end_ints = Points.objects.get(institue = end.institue, type = "5")
#                 path_to_door_from_end = Pathes.objects.get(start_point_id = end_point_id, end_point_id = door_point_end_ints)

#                 path_between_inst = Pathes.objects.get(start_point_id = door_point_start_ints, end_point_id = door_point_end_ints)

#                 return path_to_door_from_start.path.extend(
#                     path_between_inst.path).extend( # type: ignore
#                     path_to_door_from_end.path.reverse())

#             except:

#                 raw_points = raw_points.filter(Q(floor = start.floor, institue = start.institue)
#                                                 | Q(floor = end.floor, institue = end.institue)
#                                                 | Q(type = "4", institue = end.institue) | Q(type = "4", institue = end.institue)
#                                                 | Q(type = "0"))
#         else:
#             if start.floor != end.floor:
#                 raw_points = raw_points.filter(Q(floor__range = (min(start.floor, end.floor), max(start.floor, end.floor))) 
#                                                 | Q(type = "4"))
                
#             else:
#                 raw_points = raw_points.filter(floor = start.floor,
#                                                 relativeX__range = (min(start.relativeX, end.relativeX), max(start.relativeX, end.relativeX)),
#                                                 relativeY__range = (min(start.relativeY, end.relativeY), max(start.relativeY, end.relativeY)))
                

#             print(raw_points.values_list("id", "institue", "type", "relativeX", "relativeY", "connections", "floor"))

#             for point in raw_points.values_list("id", "institue", "type", "relativeX", "relativeY", "connections", "floor"):
#                 new_point = Point(point.id) #Нужны реальные данные, чтобы точнее можно было понять сортировку

#                 #TODO : Алгоритм разбиения пути на малые пути(возможное полное переписание функции)
            
class SinglyLinkedList():
    def __init__(self, point : Point, prev : SinglyLinkedList | None) -> None:
        self.point = point
        self.prev = prev

@dataclass(order=True)
class PrioritizedSinglyLinkedList:
    priority: int
    item: SinglyLinkedList=field(compare=False)

def create_path(start : Point, end : Point):
    visitedIds : set[int] = set()

    ways = queue.PriorityQueue()
    ways.put(PrioritizedSinglyLinkedList(0, SinglyLinkedList(start, None)))

    shortestWay = None

    while not ways.empty():
        way_raw = ways.get()
        way_cost = way_raw.priority
        way = way_raw.item

        for p in way.point.conns['conns']:
            if p['pk'] in visitedIds:
                continue
            visitedIds.add(p['pk'])
            try:
                newPoint = Point.objects.get(id = p['pk'])
            except:
                way.point.conns['conns'].remove(p)
                way.point.save()
                continue
            newWay = SinglyLinkedList(newPoint, way)
            distance = int(math.sqrt((newPoint.relativeX - way.point.relativeX) ** 2 + (newPoint.relativeY- way.point.relativeX) ** 2))
            ways.put(PrioritizedSinglyLinkedList(way_cost + distance, newWay))
            if p['pk'] == end.id:
                shortestWay = newWay
                break
    
    result = []
    if shortestWay is not None:
        while shortestWay.prev is not None:
            result.append(shortestWay.point)
            shortestWay = shortestWay.prev

        result.append(start)
        result.reverse()

    return result

def get_all_classrooms(institue : INSTITUES, floor : int):
    """Example of returnable data:
    {
        'pk': 1,
        'institue': 'RI',
        'type': 3,
        'x': 34,
        'y': 34,
        'floor': 1,
        'conns': [{
            'pk': 2,
            'institue': 'RI',
            'type': 2,
            'x': 44,
            'y': 44,
            'floor': 1
        }],
        'name': 'N/A'
    }
    """
    points = Point.objects.filter(institue = institue, type__in = [3, 5], floor = floor)
    points_json = [p.as_json() for p in points]
    for p_json in points_json:
        classroom = get_classroom(int(p_json['pk']))
        if classroom:
            p_json['name'] = classroom.number_of_class
        else:
            p_json["name"] = "Вход"
    return points_json

def get_classroom(id : int) -> ClassRoom | None:
    try:
        return ClassRoom.objects.get(id_of_point = id)
    except:
        return None;    