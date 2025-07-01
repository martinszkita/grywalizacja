from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField(blank=True, null=True)
    text = models.TextField()
    
    def get_random_sentence(self):
        sentences = list(self.text.split('. '))
        if not sentences:
            return ""
        import random
        return random.choice(sentences).strip()
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
