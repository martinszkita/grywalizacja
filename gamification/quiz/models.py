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
    
    
class InsertWord(models.Model):
    inserted_word = models.TextField()
    sentence = models.TextField()
    hidden_word = models.TextField()
    
    def __str__(self):
        return f"{self.inserted_word.upper()} zamiast: {self.hidden_word.upper()}, zdanie:{self.sentence[:50]} "