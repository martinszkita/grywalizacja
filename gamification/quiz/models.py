from django.db import models

class Text(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return f"{self.title}"

class Sentence(models.Model):
    id = models.BigAutoField(primary_key=True)
    text = models.ForeignKey(Text, on_delete=models.CASCADE)
    sentence = models.TextField()
    
    def __str__(self):
        return f"ID: {self.id} {self.sentence}"
    
class FillMaskData(models.Model):
    id = models.BigAutoField(primary_key=True)
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE)
    mask_index = models.IntegerField()
    mask_str = models.CharField(max_length=30)
    option1_str = models.CharField(max_length=30)
    option1_score = models.FloatField(default=-1.0000)
    option2_str = models.CharField(max_length=30)
    option2_score = models.FloatField(default=-1.0000)
    option3_str = models.CharField(max_length=30)
    option3_score = models.FloatField(default=-1.0000)
    
    def save(self, *args, **kwargs):
        words = (self.sentence.sentence).split()
        self.mask_str = words[int(self.mask_index)]
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.sentence.sentence}, {self.mask_index}"
    
class FillMaskAnswer(models.Model):
    id = models.BigAutoField(primary_key=True)
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE)
    ans = models.IntegerField() # [1 , 2, 3]
    note = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.id}, {self.ans}'
    
    
    

    
    