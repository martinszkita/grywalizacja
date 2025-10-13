from django.db import models
from django.shortcuts import HttpResponse

class Text(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=30)
    description = models.TextField(default='brak opisu')
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
class Sentence(models.Model):
    id = models.BigAutoField(primary_key=True)
    sentence = models.TextField()
    text = models.ForeignKey(Text, on_delete=models.CASCADE, related_name='sentences')
    has_data = models.BooleanField(default=False, null=True, blank=True)
    
    def __str__(self):
        return f'{self.sentence}'
    
    def check_if_has_data(self) -> bool:
        return QuestionData.objects.filter(sentence=self).exists()


    # aktualizacja pola has_data jesli Sentence jest juz uzyte do jakiegos pytania
    def save(self, *args, **kwargs):
        self.has_data = self.check_if_has_data()
        super().save(*args, **kwargs)

class QuestionData(models.Model):
    id = models.BigAutoField(primary_key=True)
    sentence = models.OneToOneField(Sentence, on_delete=models.CASCADE, related_name='data')
    options = models.JSONField()
    quiz_data = models.ForeignKey('QuizData', on_delete=models.CASCADE, related_name='datas')
    
    def __str__(self):
        return f'{self.id} {self.sentence.sentence}'
    
    def options_json_to_tuple(self):
        options_json = self.options[1:]
        choices = []
        for option in options_json:
            choices.append((option['token'], option['token']))
   
        return choices
            
class Question(models.Model):
    class QuestionType(models.IntegerChoices):
            FM = 1, "FILL_MASK"
            GR = 2, "GUESS_REPLACEMENT"
            
    id = models.BigAutoField(primary_key=True)
    question_data = models.OneToOneField(QuestionData, on_delete=models.CASCADE, related_name='question')
    question_type = models.PositiveSmallIntegerField(choices=QuestionType.choices)
    
    def __str__(self):
        return str(self.question_data)
    
class QuestionAnswer(models.Model):
    id = models.BigAutoField(primary_key=True)
    answer = models.JSONField()
    user_comment = models.TextField(null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    quiz_answer = models.ForeignKey('QuizAnswer', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.answer

class Quiz(models.Model):
    id = models.BigAutoField(primary_key=True)
    text = models.ForeignKey(Text, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.id}'

class QuizData(models.Model):
    id = models.BigAutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='data', blank=True, null=True)
    
    def __str__(self):
        return f'{self.id}'
    
class QuizAnswer(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_name = models.CharField(max_length=20,null=True, blank=True)
    user_feedback = models.SmallIntegerField(null=True, blank=True)
    user_comment = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.id}, {self.date}'