import random
import csv
from transformers import pipeline
from .models import *

DATA_PATH = '/home/marcin/grywalizacja/gamification/quiz/data/'
SENTENCES_PER_QUESTION_TYPE = 20
FILL_MASK_TOP_K = 5

def import_sentences_from_txt(filename):
    text_obj , created = Text.objects.get_or_create(title=filename)
    if created:
        text_obj.save()
    
    text = open(DATA_PATH+filename+'.txt', 'r').read()
    sentences = text.split('.')

    for i, sentence in enumerate(sentences):                
        sentence_obj = Sentence(text=text_obj, sentence=sentence)
        sentence_obj.save()
        print(f'zapisano sentence:{i, sentence_obj.sentence}')

def create_fill_mask_data():
    fill_mask = pipeline("fill-mask", model="allegro/herbert-base-cased")
    texts = Text.objects.all()
    
    for text in texts:
        for sentence in Sentence.objects.filter(text=text)[:SENTENCES_PER_QUESTION_TYPE]:
            words = sentence.sentence.split()
            if not words:
                continue
            
            mask_index = random.randint(0, len(words)-1)
            words[mask_index] = "<mask>"
            masked_sentence = " ".join(words)

            results = fill_mask(masked_sentence, top_k=FILL_MASK_TOP_K)
            options = [{'mask_index':mask_index}]+[{"token": r["token_str"], "score": round(r["score"], 4)} for r in results]

            quiz, _ = Quiz.objects.get_or_create(text=text)
            quiz_data, _ = QuizData.objects.get_or_create(quiz=quiz)

            question_data, created = QuestionData.objects.get_or_create(
                sentence=sentence,
                defaults={"quiz_data": quiz_data, "options": options}
            )

            if not created:
                question_data.options = options
                question_data.quiz_data = quiz_data
                question_data.save()


            question = Question.objects.filter(question_data__sentence=sentence).first()
            if not question:
                question = Question(
                    question_data=question_data,
                    question_type=Question.QuestionType.FM
                )
                question.save()
