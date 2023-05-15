from __future__ import annotations
from django.db import models
from django.utils.translation import gettext_lazy as _


class InstituesChoises(models.TextChoices):
    STREET = "ST", _("Улица")
    RTF = "RI", _("РИ")
    INFO = "T", _("Т")

class PointType(models.IntegerChoices):
    street = 0, _("улица")
    hall = 1, _("коридор")
    preclass = 2, _("пре аудитория")
    classroom = 3, _("аудитория")
    stairs = 4, _("лестница")
    door = 5, _("входная дверь")

# Create your models here.
class Institue(models.Model):
    name = models.CharField(max_length=2, choices=InstituesChoises.choices, verbose_name="Название")
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = "Интститут"
        verbose_name_plural = "Интституты"

class ClassRoom(models.Model):
    number_of_class = models.CharField(max_length=10, verbose_name="Номер кабинета \n Пример : РИ120")
    id_of_point = models.IntegerField()

    def __str__(self) -> str:
        return self.number_of_class
    
    class Meta:
        verbose_name = "Номер аудитории"
        verbose_name_plural = "Аудитории"

class Point(models.Model):
    def get_default_connections():
        return {"conns":[]}

    id = models.AutoField(primary_key=True)
    institue = models.CharField(max_length=2, choices=InstituesChoises.choices, default=InstituesChoises.STREET)
    type = models.IntegerField(choices=PointType.choices, default=PointType.hall)
    relativeX = models.IntegerField()
    relativeY = models.IntegerField()
    floor = models.IntegerField()
    conns = models.JSONField(default=get_default_connections)

    def __str__(self) -> str:
        if self.type == PointType.classroom.value:
            try:
                return f"{ClassRoom.objects.get(id_of_point = self.id).number_of_class}"
            except:
                return f"{self.institue} | {self.floor} | {self.relativeX} | {self.relativeY}"
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
        verbose_name = "Начальная точка ID | Конечная точка ID"
        verbose_name_plural = "Маршруты"