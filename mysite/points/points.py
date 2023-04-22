from __future__ import annotations
from points.models import Points
import math

class Point():
    def __init__(self, id : int) -> None:
        self.id = id
        try:
            point_raw = Points.objects.get(id = self.id)
        except:
            raise Exception("Can't find point")
        self.data = point_raw
        self.connections = []

    def connect(self, other_point : Point):
        self.connections.append(other_point)
        if other_point.data.type == "1" and self.data.type not in ["2", "3"]:
            other_point.connections.append(self)

class Graph():
    def __init__(self) -> None:
        self.__points = []

    @property
    def points(self):
        return self.__points
    
    def append(self, point : Point):
        self.__points.append(point)

class Data():
    def __init__(self, prev : Point | None, price : int) -> None:
        self.prev = prev
        self.price = price

def find_path(start : Point, end : Point, graph : Graph):
    not_visited = graph.points
    track = {}
    track[start] = Data(None, 0)

    while True:
        to_open : Point | None = None
        bestPrice = math.inf
        for point in not_visited:
            if point in track and track[point].price < bestPrice:
                bestPrice = track[point].price
                to_open = point

        if to_open is None:
            return None
        
        if to_open == end:
            break

        for point in to_open.connections:
            price = track[to_open].price + 1
            if point not in track or track[point].price > price:
                track[point] = Data(to_open, price)

    result = []
    while end is not None:
        result.append(end)
        end = track[end].prev

    result.reverse()
    return result