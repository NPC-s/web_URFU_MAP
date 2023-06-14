from points.models import Point, ClassRoom, Path
from enums import INSTITUES, COLORS
from PIL import Image
from django.db.models import Q


def create_points_by_pic(dir : str, institue : str, floor : int):
    img = Image.open(dir)
    counts = {"street" : 0, "hall" : 0, "preclassroom" : 0, "classroom" : 0, "stairs" : 0, "door" : 0}
    for x in range(1, img.width):
        for y in range(1, img.height):
            r, g, b, a = img.getpixel((x, y))
            hex_code = '#{:02x}{:02x}{:02x}'.format(r, g, b)
            match hex_code:
                case COLORS.STREET.value:
                    add_point_to_model(x, y, 0, institue, floor, img)
                    counts["street"]+=1
                case COLORS.HALL.value :
                    add_point_to_model(x, y, 1, institue, floor, img)
                    counts["hall"]+=1
                case COLORS.PRECLASSROOM.value :
                    add_point_to_model(x, y, 2, institue, floor, img)
                    counts["preclassroom"]+=1
                case COLORS.CLASSROOM.value :
                    add_point_to_model(x, y, 3, institue, floor, img)
                    counts["classroom"]+=1
                case COLORS.STAIRS.value :
                    add_point_to_model(x, y, 4, institue, floor, img)
                    counts["stairs"]+=1
                case COLORS.DOOR.value :
                    add_point_to_model(x, y, 5, institue, floor, img)
                    counts["door"]+=1

    img.save(dir)
    
    return counts
    

def add_point_to_model(x : int, y : int, type : int, institue : str, floor : int, img : Image):
    img.putpixel((x, y), (0, 0, 0, 0))
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

def connect_point_other_types(start_type : int, end_type : int, institue : INSTITUES, floor : int):
    start_points = Point.objects.filter(type = start_type, institue = institue, floor = floor)
    for point in start_points:
        end_points = Point.objects.filter(relativeX = point.relativeX, type = end_type, institue = institue, floor = floor)
        searching_by = "X"
        if len(end_points) == 0:
            end_points = Point.objects.filter(relativeY = point.relativeY, type = end_type, institue = institue, floor = floor)
            searching_by = "Y"
            if len(end_points) == 0:
                print(point.relativeX, point.relativeY, "не нашел совпадений")
                continue

        if len(end_points) == 1:
            point.connect(end_points[0])
        
        else:
            if searching_by == "X":
                sorted_preclassrooms = sorted(end_points, key = lambda precl : abs(precl.relativeY - point.relativeY))
            else:
                sorted_preclassrooms = sorted(end_points, key = lambda precl : abs(precl.relativeX - point.relativeX))
            point.connect(sorted_preclassrooms[0])

def connect_point_one_type(type : int, institue : INSTITUES, floor : int):
    points = Point.objects.filter(type = type, institue = institue, floor = floor)
    for point in points:
        points_on_lines = points.filter(Q(relativeX = point.relativeX) | Q(relativeY = point.relativeY))
        for p in points_on_lines:
            point.connect(p)

def delete_point(institue : INSTITUES, floor : int):
    classrooms = Point.objects.filter(institue = institue, floor = floor, type = 3).values_list("pk", flat=True)
    ClassRoom.objects.filter(id_of_point__in = classrooms).delete()
    Path.objects.filter(Q(start_point_id__in = classrooms) | Q(end_point_id__in = classrooms)).delete()
    Point.objects.filter(institue = institue, floor = floor).delete()
