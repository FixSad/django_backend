from django import forms
from test_django.models import Car, Mechanic, Client, Message


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ('name', 'mileage', 'malfunction', 'mechanics')


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('first_name', 'surname', 'city', 'phone_number')


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('title', 'body')


class MechanicForm(forms.ModelForm):
    class Meta:
        model = Mechanic
        fields = ('first_name', 'surname', 'experience', 'department', 'rating')











