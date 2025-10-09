from django.db import models

class Text(models.Model):
    class QuestionType(models.TextChoices):
        FILL_MASK = "FM", "FM"
        GUESS_REPLACEMENT =  "GR", "GR"
        
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='text_images/', blank=True, null=True)
    question_type = models.CharField(max_length=100, choices=QuestionType.choices)

    class Meta:
        unique_together = ('title', 'question_type')
    
    def __str__(self):
        return f"{self.title}"
    
class Quiz(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now=True)
    texts = models.ManyToManyField(Text, related_name='quizzes')
    
    def __str__(self):
        return f'{self.id}'
    
class Sentence(models.Model):
    id = models.BigAutoField(primary_key=True)
    text = models.ForeignKey(Text, on_delete=models.CASCADE, related_name='sentences')
    sentence = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f"{self.id}"

class FillMaskData(models.Model):
    id = models.BigAutoField(primary_key=True)
    sentence = models.OneToOneField(Sentence, on_delete=models.CASCADE, related_name="fill_mask_data")
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
        return f"{self.id}"
    
class FillMaskAnswer(models.Model):
    id = models.BigAutoField(primary_key=True)
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE, related_name="answers")
    ans = models.IntegerField() # [1 , 2, 3]
    note = models.CharField(max_length=200, blank=True, null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f'{self.sentence.text}, {self.id}, {self.note}'
    
class GuessReplacementData(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_replacement = models.BooleanField()
    replacement_index = models.IntegerField(null=True, blank=True, default=-1)
    replacing_str = models.CharField(max_length=25, null=True, blank=True)
    sentence = models.OneToOneField(Sentence, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.id},{self.sentence}, {self.is_replacement}'
    
class GuessReplacementAnswer(models.Model):
    id = models.BigAutoField(primary_key=True)
    ans = models.BooleanField() # 1 - replacement, 0 - no replacement
    ans_correct = models.BooleanField()
    note = models.CharField(max_length=200, blank=True, null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.id}, ans: {self.ans}'