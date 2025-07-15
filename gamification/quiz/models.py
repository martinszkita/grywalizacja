from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField(blank=True, null=True)
    text = models.TextField()
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
class WordRating(models.Model):
    rated_word = models.CharField(max_length=50)
    value = models.IntegerField(default=0)
    sentence = models.TextField()
    
    def __str__(self):
        return f"{self.rated_word.upper()} rating:{self.value}, {self.sentence}"