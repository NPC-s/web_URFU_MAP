from django.db import models
from django.utils.translation import gettext_lazy as _
import json


class InstituesChoises(models.TextChoices):
        STREET = "ST", _("Улица")
        RTF = "RI", _("РИ")
        INFO = "T", _("Т")

# Create your models here.
class Institues(models.Model):
    name = models.CharField(max_length=2, choices=InstituesChoises.choices, verbose_name="Название")
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = "Интститут"
        verbose_name_plural = "Интституты"

class ClassRooms(models.Model):
    number_of_class = models.CharField(max_length=10, verbose_name="Номер кабинета \n Пример : РИ120")
    id_of_point = models.IntegerField()

    def __str__(self) -> str:
        return self.number_of_class
    
    class Meta:
        verbose_name = "Номер аудитории"
        verbose_name_plural = "Аудитории"

class Points(models.Model):
    class PointType(models.TextChoices):
        street = "0", _("улица")
        hall = "1", _("коридор")
        preclass = "2", _("пре аудитория")
        classroom = "3", _("аудитория")

    def connections_default():
        return {"connections" : []}

    institue = models.CharField(max_length=2, choices=InstituesChoises.choices, default=InstituesChoises.STREET)
    type = models.CharField(max_length=1, choices=PointType.choices, default=PointType.hall)
    relativeX = models.IntegerField()
    relativeY = models.IntegerField()
    connections = models.JSONField(default=connections_default())
    floor = models.IntegerField()

    
    class Meta:
        verbose_name = "Тип точки | Этаж"
        verbose_name_plural = "Точки"

