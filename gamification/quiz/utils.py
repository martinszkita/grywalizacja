import csv
from .models import *

SENTENCE_FILE_PATH = '/home/marcin/grywalizacja/gamification/quiz/data/dolphins_sentences.csv'
MASK_DATA_FILE_PATH = '/home/marcin/grywalizacja/gamification/quiz/data/dolphins_mask_data.csv'

text = Text.objects.get(title='Delfiny')

def import_sentences():
    with open(SENTENCE_FILE_PATH, 'r') as f:
        reader = csv.DictReader(f)
        for r in reader:
            sentence = Sentence(sentence = r['sentence'], text=text)
            sentence.save()
            

def import_fill_mask_data():
    with open(MASK_DATA_FILE_PATH, 'r') as f:
        reader = csv.DictReader(f)
        for i, r in enumerate(reader):
            args = {}
            args['option1_str'] = r['option1_str']
            args['option1_score'] = r['option1_score']
            args['option2_str'] = r['option2_str']
            args['option2_score'] = r['option2_score']
            args['option3_str'] = r['option3_str']
            args['option3_score'] = r['option3_score']
            args['mask_index'] = r['mask_index']
            args['sentence'] = Sentence.objects.get(pk=i+1)
            
            fill_mask_data_object = FillMaskData(**args)
            fill_mask_data_object.save()
            
    

    
            
            

