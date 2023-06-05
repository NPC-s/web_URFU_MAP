from django import forms
from points.models import MapImages

class MapImageForm(forms.ModelForm):
    class Meta:
        model = MapImages
        fields = ('image', "floor", "institue")

    def save(self, commit=True):
        instance = super().save(commit=False)
        new_filename = f'{self.cleaned_data["institue"]}_{self.cleaned_data["floor"]}.jpg'
        instance.image.name = new_filename

        if commit:
            instance.save()
        
        return instance