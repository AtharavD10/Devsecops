from django.db import models

# Create your models here.
class Contact(models.Model):
    name= models.CharField(max_length=122)
    email= models.CharField(max_length=122)
    phone= models.CharField(max_length=12)
    queries= models.TextField()
    date= models.DateField()

    def __str__(self):
        return self.name

class Diet(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=100)
    calories = models.IntegerField()

    def __str__(self):
        return self.name