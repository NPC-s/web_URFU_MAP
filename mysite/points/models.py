from __future__ import annotations
from django.db import models
from enums import InstituesChoices, PointChoices
from PIL import Image
from detect_pixel_on_line import get_path_of_static_file


class Institue(models.Model):
    name = models.CharField(max_length=2, choices=InstituesChoices.choices, verbose_name="Название")
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = "Интститут"
        verbose_name_plural = "Интституты"
        db_table = "Institues"

class ClassRoom(models.Model):
    number_of_class = models.CharField(max_length=10, verbose_name="Номер кабинета \n Пример : РИ 120")
    id_of_point = models.IntegerField()

    def __str__(self) -> str:
        return self.number_of_class
    
    class Meta:
        verbose_name = "Номер аудитории"
        verbose_name_plural = "Аудитории"
        db_table = "Classrooms"

class Point(models.Model):
    def get_default_connections():
        return {"conns":[]}

    id = models.AutoField(primary_key=True)
    institue = models.CharField(max_length=2, choices=InstituesChoices.choices, default=InstituesChoices.STREET)
    type = models.IntegerField(choices=PointChoices.choices, default=PointChoices.HALL)
    relativeX = models.IntegerField()
    relativeY = models.IntegerField()
    floor = models.IntegerField()
    conns = models.JSONField(default=get_default_connections)

    def __str__(self) -> str:
        if self.type == PointChoices.CLASSROOM.value:
            try:
                return f"{ClassRoom.objects.get(id_of_point = self.id).number_of_class}"
            except:
                pass
        return f"{self.institue} | {self.floor} | {self.relativeX} | {self.relativeY}"
    
    def as_json(self, is_full : bool = True):
        result = dict(
            pk = self.id,
            institue = self.institue,
            type = self.type,
            x = self.relativeX,
            y = self.relativeY,
            floor = self.floor,
        )
        if is_full:
            result["conns"] = self.conns['conns']
        return result

    class Meta:
        verbose_name = "Институт | Этаж | X | Y или Номер кабинета"
        verbose_name_plural = "Точки"
        db_table = "Points"

    def connect(self, other : Point):
        if ((self.relativeX == other.relativeX and self.relativeY == other.relativeY) or (self.relativeX != other.relativeX and self.relativeY != other.relativeY)) and self.type != 4:
            return


        if (self.type == 4 and other.type == 4) or not self.is_line_contains_wall(other):
            if self.id not in [p['pk'] for p in other.conns['conns']]:
                other.conns['conns'].append(self.as_json(False))
                other.save()
            if other.id not in [p['pk'] for p in self.conns['conns']]:
                self.conns['conns'].append(other.as_json(False))
                self.save()

    def disconnect(self, other : Point):
        if ((self.relativeX == other.relativeX and self.relativeY == other.relativeY) or (self.relativeX != other.relativeX and self.relativeY != other.relativeY)) and self.type != 4:
            return

        if self.id in [p['pk'] for p in other.conns['conns']]:
            other.conns['conns'].remove(self.as_json(False))
            other.save()
        if other.id in [p['pk'] for p in self.conns['conns']]:
            self.conns['conns'].remove(other.as_json(False))
            self.save()
    
    def is_line_contains_wall(self, other : Point):
        if self.floor != other.floor or self.institue != other.institue:
            return True

        if self.relativeX == other.relativeX:
            deltaY = -1 if self.relativeY > other.relativeY else 1
            deltaX = 0
        elif self.relativeY == other.relativeY:
            deltaX = -1 if self.relativeX > other.relativeX else 1
            deltaY = 0
        else:
            return True

        x, y = self.relativeX + deltaX, self.relativeY + deltaY

        image_url = MapImages.objects.get(institue = self.institue, floor = self.floor).image.url
        image = Image.open(get_path_of_static_file(image_url))

        while True:
            if other.relativeX == x and other.relativeY == y:
                return False
            
            if image.getpixel((x, y)) == (0, 0, 0, 255):
                return True
        
            x += deltaX
            y += deltaY




class Path(models.Model):
    def get_default_pathes():
        return {"pathes":[]}

    start_point_id = models.IntegerField()
    end_point_id = models.IntegerField()

    path = models.JSONField(default=get_default_pathes)

    def __str__(self) -> str:
        return f"{str(Point.objects.get(self.start_point_id))} | {str(Point.objects.get(self.end_point_id))}"

    class Meta:
        verbose_name = "Начальная точка | Конечная точка"
        verbose_name_plural = "Маршруты"
        db_table = "Pathes"

class MapImages(models.Model):
    institue = models.CharField(max_length=2, choices=InstituesChoices.choices, default=InstituesChoices.STREET, verbose_name="Институт")
    floor = models.IntegerField(verbose_name="Этаж")
    image = models.ImageField(upload_to="static/images/maps/", verbose_name="Файл")
    is_have_points = models.BooleanField(verbose_name="Наличие точек в бд", default=False)

    class Meta:
        db_table = "Images_Map"