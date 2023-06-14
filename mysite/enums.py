from typing import Literal
from django.db import models
from django.utils.translation import gettext_lazy as _
import enum


INSTITUES = Literal["RI"]

class COLORS(enum.Enum):
    STREET = "#23234214134"
    HALL = "#2400ff"
    PRECLASSROOM = "#fa05f0"
    CLASSROOM = "#00ffff"
    STAIRS = "#00ff00"
    DOOR = "#ff1111"

class InstituesChoices(models.TextChoices):
    STREET = "ST", _("Улица")
    RTF = "RI", _("РИ")
    INFO = "T", _("Т")
    GUK = "GK", _("ГУК")

class PointChoices(models.IntegerChoices):
    STREET = 0, _("улица")
    HALL = 1, _("коридор")
    PRECLASS = 2, _("перед аудиторией")
    CLASSROOM = 3, _("аудитория")
    STAIRS = 4, _("лестница")
    DOOR = 5, _("входная дверь")