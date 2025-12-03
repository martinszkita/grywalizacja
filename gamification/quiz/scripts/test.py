from quiz.models import *

def run():
    print(Sentence.objects.first().has_data)