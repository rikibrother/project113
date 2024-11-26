from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver

# Create your models here.
class student(models.Model):
    name = models.CharField(max_length=25)
    age = models.IntegerField(default=18)
    marks= models.DecimalField(max_digits=8, decimal_places=2)
    course = models.CharField(max_length=20, choices=[
        ('Python', 'Python'),
        ('AI', 'AI'),
        ('Jave', 'Jave'),
        
    ])
    
    def __str__(self):
        return self.name


# model to fetch profile picture while user is signing up

class Extended(models.Model):
    id =models.OneToOneField(User,primary_key=True, on_delete=models.CASCADE)
    image = models.ImageField()
    
    def __str__(self):
        return str(self.id)
    


import os
@receiver(pre_delete, sender=User)  #post delete can also be used
def delete_picture(sender, instance, **kwargs):
    try:
        os.remove(instance.extended.image.path)
    except:
        pass
    


class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=4, null=True)
    rated = models.CharField(max_length=10, null=True)
    released = models.DateField(null=True)
    runtime = models.CharField(max_length=50, null=True)
    genre = models.CharField(max_length=255, null=True)
    director = models.CharField(max_length=255, null=True)
    writer = models.CharField(max_length=255, null=True)
    actors = models.TextField(null=True)
    plot = models.TextField(null=True)
    language = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    awards = models.CharField(max_length=255, null=True)
    poster = models.URLField(null=True)
    metascore = models.IntegerField(null=True)
    imdb_rating = models.FloatField(null=True)
    imdb_votes = models.CharField(max_length=20, null=True)
    imdb_id = models.CharField(max_length=20, null=True)
    type = models.CharField(max_length=50, null=True)
    response = models.BooleanField(default=True)

    def __str__(self):
        return self.title
