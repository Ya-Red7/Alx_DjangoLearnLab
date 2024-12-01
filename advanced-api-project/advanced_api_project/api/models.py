from django.db import models

# Create your models here.
class Author(models.Model):
    # this class has a field
    name = models.CharField(max_length = 200)
# Author is related to Book by one-to-many relationship
class Book(models.Model):
    #this class has 3 fields, one is foreign key to the author class
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)