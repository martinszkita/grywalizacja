import random
import csv
from transformers import pipeline
from .models import Text, Sentence, FillMaskData

DIR = '/home/marcin/grywalizacja/gamification/quiz/data/'

def full_fill_mask_import(filename: str, max_sentences: int = 20):
    # 1. utwórz obiekt Text jeśli nie istnieje
    text_obj, created = Text.objects.get_or_create(title=filename)

    # 2. wczytaj zdania z pliku
    with open(DIR + filename + '.txt', 'r') as f:
        raw_sentences = f.read().split('.')

    sentences = [s.strip() for s in raw_sentences if s.strip()][:max_sentences]

    # 3. pipeline HuggingFace (HerBERT)
    fill_mask = pipeline("fill-mask", model="allegro/herbert-base-cased")

    # 4. przygotuj CSV
    csv_path = DIR + filename + '.csv'
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
