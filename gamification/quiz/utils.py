import csv
from .models import *

SENTENCE_FILE_PATH = '/home/marcin/grywalizacja/gamification/quiz/data/dolphins_sentences.csv'
MASK_DATA_FILE_PATH = '/home/marcin/grywalizacja/gamification/quiz/data/dolphins_mask_data.csv'

def import_sentences():
    with open(SENTENCE_FILE_PATH, 'r') as f:
        reader = csv.DictReader(f)
        text = Text.objects.get(title='Delfiny')
        if not text:
            text=Text(title='Delfiny')
            print("nie ma modelu")
        for r in reader:
            sentence = Sentence(sentence = r['sentence'], text=text)
            sentence.save()
    

    
            
            

