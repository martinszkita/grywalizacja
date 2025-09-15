from django.db import models

class Text(models.Model):
    title = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.title}"

class Sentence(models.Model):
    text = models.ForeignKey(Text, on_delete=models.CASCADE)
    sentence = models.TextField()
    
    def __str__(self):
        return f"{self.sentence}"
    
class FillMaskData(models.Model):
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE)
    mask_index = models.IntegerField()
    mask_str = models.CharField(max_length=30, editable=False, blank=True, null=True)
    option1_str = models.CharField(max_length=30)
    option1_score = models.FloatField(default=-1.0000)
    option2_str = models.CharField(max_length=30)
    option2_score = models.FloatField(default=-1.0000)
    option3_str = models.CharField(max_length=30)
    option3_score = models.FloatField(default=-1.0000)
    
    def save(self, *args, **kwargs):
        words = (self.sentence.sentence or "").split()
        if 0 <= self.mask_index < len(words):
            self.mask_str = words[self.mask_index]
        else:
            self.mask_str = ""  
        super().save(*args, **kwargs)
    
    
    def __str__(self):
        return f"Pytanie delfiny"
    
class FillMaskAnswer(models.Model):
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE)
    ans = models.IntegerField() # [1 , 2, 3]
    note = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"text:{self.sentence.text.title}, sent_id:{self.sentence.id},ans:{self.ans} ..."
    