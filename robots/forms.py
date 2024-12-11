from typing import Dict, Any

from django import forms
from .models import Robot


class RobotForm(forms.ModelForm):
    class Meta:
        model = Robot
        fields = ['model', 'version', 'created']
        widgets = {
            'created': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
            }),
        }

    def clean(self) -> Dict[str, Any]:
        clean_data = super().clean()
        model = clean_data.get('model')
        version = clean_data.get('version')

        if len(model) != 2 or len(version) != 2:
            raise forms.ValidationError("Model and version must be 2 characters long.")

        return clean_data