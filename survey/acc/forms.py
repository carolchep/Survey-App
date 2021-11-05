from django import forms
from .models import Survey, Question, TextField





class SurveyForm(forms.ModelForm):

    class Meta:

        model = Survey
        fields = ["title"]

class TextForm(forms.ModelForm):

    class Meta:

        model = Question,Textform
        fields = ["question","input"]


class FloatForm(forms.ModelForm):
    
    class Meta:
        model=Float,Question
        fields = ["question","input"]


class Dropdown(forms.ModelForm):

    class Meta:
        model=Questiom,Dropdown
        fields = ["question","input"]



