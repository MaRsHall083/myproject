from django.db import models

# Create your models here.
from django.db import models

class Question(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    scale = models.CharField(max_length=50)

    def __str__(self):
        return self.text

class Result(models.Model):
    name = models.CharField(max_length=100)
    scale_a = models.IntegerField(default=0)
    scale_b = models.IntegerField(default=0)
    scale_c = models.IntegerField(default=0)
    scale_d = models.IntegerField(default=0)
    scale_e = models.IntegerField(default=0)

    def __str__(self):
        return self.name