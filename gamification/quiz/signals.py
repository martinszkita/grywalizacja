from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import *

@receiver(post_delete, sender=QuestionData)
def update_sentence_after_question_data_removed(sender, instance, **kwargs):
    print('SIGNAL: update_sentence_after_question_data_removed')
    instance.sentence.save() # instance to QuestionData
