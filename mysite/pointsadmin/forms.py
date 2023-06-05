from django import forms
from enums import InstituesChoices

class MapImageEditForm(forms.Form):
    CHOICES = [
        ('delete', 'Удалить'),
        ('update', 'Изменить'),
        ('create_points', 'Создать и объединить точки'),
    ]
    pk = forms.IntegerField(label = "ID", required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    do = forms.ChoiceField(label ="Действия", choices=CHOICES, required=True)

    floor = forms.IntegerField(label="Этаж", required=False)
    institue = forms.ChoiceField(label="Институт", choices=[(choice.value, choice.name) for choice in InstituesChoices], required=False)