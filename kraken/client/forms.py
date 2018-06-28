from django import forms

class ContactForm(forms.Form):
    iteration = forms.IntegerField()
