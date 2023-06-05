from __future__ import annotations
from django.db import models
from enums import InstituesChoices, PointChoices

# Create your models here.
class Institue(models.Model):
    name = models.CharField(max_length=2, choices=InstituesChoices.choices, verbose_name="Название")
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = "Интститут"
        verbose_name_plural = "Интституты"

class ClassRoom(models.Model):
    number_of_class = models.CharField(max_length=10, verbose_name="Номер кабинета \n Пример : РИ 120")
    id_of_point = models.IntegerField()

    def __str__(self) -> str:
        return self.number_of_class
    
    class Meta:
        verbose_name = "Номер аудитории"
        verbose_name_plural = "Аудитории"

class Point(models.Model):
    def get_default_connections(self):
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

    class Meta:
        verbose_name = "Институт | Этаж | X | Y или Номер кабинета"
        verbose_name_plural = "Точки"

    def connect(self, other : Point):
        if self.id not in other.conns['conns']:
            other.conns['conns'].append(self.id)
            other.save()
        if other.id not in self.conns['conns']:
            self.conns['conns'].append(other.id)
            self.save()

class Path(models.Model):
    def get_default_pathes(self):
        return {"pathes":[]}

    start_point_id = models.IntegerField()
    end_point_id = models.IntegerField()

    path = models.JSONField(default=get_default_pathes)

    def __str__(self) -> str:
        return f"{str(Point.objects.get(self.start_point_id))} | {str(Point.objects.get(self.end_point_id))}"

    class Meta:
        verbose_name = "Начальная точка | Конечная точка"
        verbose_name_plural = "Маршруты"

class MapImages(models.Model):
    institue = models.CharField(max_length=2, choices=InstituesChoices.choices, default=InstituesChoices.STREET, verbose_name="Институт")
    floor = models.IntegerField(verbose_name="Этаж")
    image = models.ImageField(upload_to="static/images/maps/", verbose_name="Файл")