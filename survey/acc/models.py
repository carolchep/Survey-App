from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone


# Create your models here
class Survey(models.Model):

    #user creates a survey

    title = models.CharField(max_length=64)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


class Question(models.Model):

    """A question in a survey"""
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=128)
    def __str__(self):

        return self.question
 
class TextField(model.Model):
    "'A text field input"
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    input= models.CharField(max_length=200)
    
class Float(model.Model):
    'A floating  field input'
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    
class Options(model.Model):
    'A floating  field input'
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    
class Submission(models.Model):

    """A set of answers a survey's questions."""
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    

 
