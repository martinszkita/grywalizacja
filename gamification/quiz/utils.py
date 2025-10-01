import random
import csv
from transformers import pipeline
from .models import Text, Sentence, FillMaskData, GuessReplacementData

FILL_MASK_DIR = '/home/marcin/grywalizacja/gamification/quiz/data/fill_mask/'
GUESS_REPLACEMENT_DIR = '/home/marcin/grywalizacja/gamification/quiz/data/guess_replacement/'
MAX_SENTENCES = 20

def full_fill_mask_import(filename: str):
    # 1. utwórz obiekt Text jeśli nie istnieje
    text_obj, created = Text.objects.get_or_create(title=filename)

    # 2. wczytaj zdania z pliku
    with open(FILL_MASK_DIR + filename + '.txt', 'r') as f:
        raw_sentences = f.read().split('.')

    sentences = [s.strip() for s in raw_sentences if s.strip()][:MAX_SENTENCES]

    # 3. pipeline HuggingFace (HerBERT)
    fill_mask = pipeline("fill-mask", model="allegro/herbert-base-cased")

    # 4. przygotuj CSV
    csv_path = FILL_MASK_DIR + filename + '.csv'
    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = [
            'sentence', 'mask_index', 'mask_str',
            'option1_str', 'option1_score',
            'option2_str', 'option2_score',
            'option3_str', 'option3_score'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # 5. iteruj po zdaniach
        for s in sentences:
            words = s.split()
            if not words:
                continue

            # wybór słowa do zamaskowania
            mask_index = random.randrange(len(words))
            mask_str = words[mask_index]
            words[mask_index] = '<mask>'
            masked_sentence = " ".join(words)

            # predykcje
            results = fill_mask(masked_sentence, top_k=3)

            # zapis do bazy
            sentence_obj = Sentence.objects.create(
                text=text_obj,
                sentence=s
            )

            FillMaskData.objects.create(
                sentence=sentence_obj,
                mask_index=mask_index,
                mask_str=mask_str,
                option1_str=results[0]['token_str'],
                option1_score=round(results[0]['score'], 4),
                option2_str=results[1]['token_str'],
                option2_score=round(results[1]['score'], 4),
                option3_str=results[2]['token_str'],
                option3_score=round(results[2]['score'], 4),
            )

            # zapis do CSV
            writer.writerow({
                'sentence': s,
                'mask_index': mask_index,
                'mask_str': mask_str,
                'option1_str': results[0]['token_str'],
                'option1_score': round(results[0]['score'], 4),
                'option2_str': results[1]['token_str'],
                'option2_score': round(results[1]['score'], 4),
                'option3_str': results[2]['token_str'],
                'option3_score': round(results[2]['score'], 4),
            })

    print(f"✅ Zapisano quiz '{filename}' ({len(sentences)} zdań) do bazy i pliku {csv_path}")

def full_guess_replacement_import(filename: str):
    text_obj, created = Text.objects.get_or_create(title=filename, question_type=Text.QuestionType.GUESS_REPLACEMENT)

    # zapis zdan do bazy
    with open(GUESS_REPLACEMENT_DIR+filename+'.txt', 'r', newline='') as f:
        raw_sentences = f.read().split('.')
        
    sentences = [sentence.strip() for sentence in raw_sentences if sentence.strip()][:MAX_SENTENCES]

    # przygotowanie pliku csv z danymi
    with open(GUESS_REPLACEMENT_DIR+filename+'.csv', 'w', newline='') as f:
        field_names = ['text', 'sentence_id', 'is_replacement', 'replaced_index','replaced_str']
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        
        for i, s in enumerate(sentences):
            s = Sentence(text=text_obj, sentence=s)
            s.save()
            sentence_list = s.sentence.split()
            is_replacement = random.choice([True, False])
            
            if is_replacement:
                replacement_index = random.randint(0, len(sentence_list) - 1)
                sentence_masked = sentence_list
                sentence_masked[replacement_index] = '<mask>'
                sentence_masked = ' '.join(sentence_masked)
                fill_mask = pipeline("fill-mask", model="allegro/herbert-base-cased")
                results = fill_mask(sentence_masked, top_k=5)
                replacement_str = results[4]['token_str']
            else:
                replacement_index = -1
                replacement_str = ''
                
            writer.writerow({
                'text':text_obj,
                'sentence_id':s.id,
                'is_replacement': is_replacement,
                'replaced_index': replacement_index,
                'replaced_str': replacement_str
            })
            guess_replacement_data = GuessReplacementData(
                is_replacement = is_replacement,
                replacing_str = replacement_str,
                sentence = s,
                replacement_index = replacement_index
            )
            
            guess_replacement_data.save()
    
    print(f"✅ Zapisano ({len(sentences)} zdań) do bazy i pliku csv")
    