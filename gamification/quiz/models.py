from django.db import models

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
    
    def __str__(self):
        return f'{self.id} {self.sentence}'

class QuestionData(models.Model):
    id = models.BigAutoField(primary_key=True)
    sentence = models.OneToOneField(Sentence, on_delete=models.CASCADE)
    options = models.JSONField()
    quiz_data = models.ForeignKey('QuizData', on_delete=models.CASCADE, related_name='data')
    
    def __str__(self):
        return self.options

class Question(models.Model):
    class QuestionType(models.IntegerChoices):
            FM = 1, "FILL_MASK"
            GR = 2, "GUESS_REPLACEMENT"
            
    id = models.BigAutoField(primary_key=True)
    question_data = models.OneToOneField(QuestionData, on_delete=models.CASCADE)
    question_type = models.PositiveSmallIntegerField(choices=QuestionType.choices)
    
    def __str__(self):
        return str(self.question_data)
    
class QuestionAnswer(models.Model):
    id = models.BigAutoField(primary_key=True)
    answer = models.JSONField()
    user_comment = models.TextField()
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
    user_name = models.CharField(max_length=20)
    user_feedback = models.SmallIntegerField()
    user_comment = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.id}, {self.date}'