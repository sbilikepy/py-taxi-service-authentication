from django import forms
from django.db import models
from .models import *


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        # fields = ("row","row")
