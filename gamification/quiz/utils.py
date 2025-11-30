import os
import django
from collections import Counter
from operator import itemgetter

# do ladnego printowania
from pprint import pprint

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gamification.settings")
django.setup()

import random

# from transformers import pipeline
# import morfeusz2
# import plwordnet
# import pickle

from .models import *

DATA_PATH = "/home/marcin/grywalizacja/gamification/quiz/data/"
SENTENCES_PER_QUESTION_TYPE = 20
FILL_MASK_TOP_K = 5
WHICH_BEST_FILL_MASK_ANSWER = (
    3  # ktora najlespza z kolei opcja do wybrania z fill_mask()
)

# morf = morfeusz2.Morfeusz()
# with open("/home/marcin/grywalizacja/wordnet.pkl", "rb") as f:
#     wn = pickle.load(f)

SKIP_WORDS = """
a acz aczkolwiek aż albo ale ani aniżeli aby bowiem bądź bo by był była było byli bez bardziej bardzo będą będzie będący będąca będące
czasem czasami czy czyż dla dlatego do dokąd dobrze dużo dzisiaj dziś gdy gdyby gdyż gdzie gdzieś gdziekolwiek iż
jak jakby jako jakiś jakkolwiek jakoś jakże jest jeszcze już jeżeli jeśli każdy każda każde każdym kiedy kilka kilkanaście kilkadziesiąt
lub lecz ma mają mam mamy może mogą możesz nad nade nawet na nie niech niestety nigdy nigdzie nikomu nikogo no o od ode około oraz oto
po pod pode podczas poza potem ponieważ przed przede przez przy przecież raz razem sam sama samo sami same są skąd tak także tam też tylko tyle toteż trudno
tu tutaj tymczasem u w we więc wobec właśnie wciąż wszyscy wszystkie wszystko z za zamiast zawsze zanim zatem zaś ze żeby że żaden żadna żadne żadnych
jakikolwiek kiedykolwiek gdziekolwiek dokądkolwiek jakkolwiek ilekolwiek mniej więcej prawie chyba może trochę przynajmniej bynajmniej tudzież jedynie to Ale w i
""".split()


def import_sentences_from_txt(filename):  # podac tylko np. 'maroko' albo 'delfiny'
    text_obj, created = Text.objects.get_or_create(title=filename)
    if created:
        text_obj.save()

    text = open(DATA_PATH + filename + ".txt", "r").read()
    sentences = text.split(".")
    saved = 0

    for i, sentence in enumerate(sentences):
        sentence_obj = Sentence(text=text_obj, sentence=sentence)
        if sentence_obj.sentence:
            sentence_obj.save()
            saved += 1

    print(f"zaimportowano {saved} sentences z pliku {filename}")

def create_fill_mask_data_herbert():
    fill_mask = pipeline("fill-mask", model="allegro/herbert-base-cased")
    texts = Text.objects.all()

    for text in texts:
        for sentence in Sentence.objects.filter(text=text)[
            :SENTENCES_PER_QUESTION_TYPE
        ]:
            words = sentence.sentence.split()
            if not words:
                continue

            mask_index = random.randint(0, len(words) - 1)
            mask_str = words[mask_index]
            words[mask_index] = "<mask>"
            masked_sentence = " ".join(words)

            results = fill_mask(masked_sentence, top_k=FILL_MASK_TOP_K)
            question_data = {
                "mask_index": mask_index,
                "options": [
                    {
                        "token": r["token_str"],
                        "score": round(r["score"], 4),
                        "source": "herbert",
                    }
                    for r in results
                    # tutaj dojda jeszcze dane z wordnetu
                ],
            }

            quiz, _ = Quiz.objects.get_or_create(text=text)
            quiz_data, _ = QuizData.objects.get_or_create(quiz=quiz)

            question_data, created = QuestionData.objects.get_or_create(
                sentence=sentence,
                defaults={"quiz_data": quiz_data, "question_data": question_data},
            )

            if not created:
                question_data.options = options
                question_data.quiz_data = quiz_data
                question_data.save()

            question = Question.objects.filter(question_data__sentence=sentence).first()

            if not question:
                question = Question(
                    question_data=question_data, question_type=Question.QuestionType.FM
                )
            question.save()
            print(f"Zapisano question: {question.id}")

def create_guess_replacement_data():
    fill_mask = pipeline("fill-mask", model="allegro/herbert-base-cased")
    saved_GR_data = 0

    for text in Text.objects.all():
        sentences_without_data = Sentence.objects.filter(text=text, has_data=False)
        question_count = min(
            sentences_without_data.count(), SENTENCES_PER_QUESTION_TYPE
        )
        quiz, _ = Quiz.objects.get_or_create(text=text)
        quiz_data, _ = QuizData.objects.get_or_create(quiz=quiz)

        for sentence in sentences_without_data[:question_count]:
            question_data_o = QuestionData()
            question_data_o.quiz_data = quiz_data

            if QuestionData.objects.filter(sentence=sentence).exists():
                raise Exception(f"sentence z id: {sentence.id} juz w uzyciu!")

            question_data_o.sentence = sentence

            # przygotowanie options:JSON
            is_replacement = random.choice([True, False])
            question_data = dict()

            question_data["is_replacement"] = is_replacement

            if is_replacement:
                sentence_list = sentence.sentence.split()
                s_len = len(sentence_list)
                replacement_index = random.randint(0, s_len - 1)
                sentence_list[replacement_index] = "<mask>"
                results = fill_mask(" ".join(sentence_list), top_k=FILL_MASK_TOP_K)

                question_data["replacement_index"] = replacement_index
                question_data["choices"] = []

                # dodanie danych z herberta
                for result in results:
                    choice = {}
                    choice["replacement_str"] = result["token_str"]
                    choice["replacement_score"] = result["score"]
                    choice["which_best"] = WHICH_BEST_FILL_MASK_ANSWER
                    choice["source"] = "herbert"
                    question_data["choices"].append(choice)

                # dodanie synonimów z wordnetu
                replacement_str = sentence_list[replacement_index]
                synonyms = get_synonyms(replacement_str)

                for synonym in synonyms:
                    question_data["choices"].append(
                        {"replacement_str": synonym, "source": "wordnet"}
                    )

            question_data_o.question_data = question_data
            question_data_o.save()
            saved_GR_data += 1

            question = Question()
            question.question_data = question_data_o
            question.question_type = Question.QuestionType.GR
            question.save()
            sentence.save()

    print(f"zapisano {saved_GR_data} question_data obiektów")

def get_base_form_and_tag(word):
    # morf = morfeusz2.Morfeusz()
    analyses = morf.analyse(word)

    if not analyses:
        return {"base_form": word, "form_tag": None}

    # wybieramy pierwszą interpretację
    _, _, interp = analyses[0]

    return {"base_form": interp[1].split(":")[0], "form_tag": interp[2]}

def get_synonyms(word):
    def generate_given_form(word, tag):
        resolver = morf._morfeusz_obj.getIdResolver()
        tag_id = resolver.getTagId(tag)

        for orth, lemma, tag, name, labels in morf.generate(word, tag_id):
            return orth

    base_form = get_base_form_and_tag(word)["base_form"].split(":")[0]
    base_form_tag = get_base_form_and_tag(word)["form_tag"]
    synset = get_synset_words(base_form)
    new_forms = set()

    for s in synset:
        new_form = generate_given_form(s, base_form_tag)
        if new_form is None or new_form == word:
            continue
        new_forms.add(new_form)

    return new_forms
 
# zaklada ze sa juz dane z herberta!!!
def refill_fill_mask_data_wordnet():
    questions_saved = 0
    synonyms_saved = 0
    for qd in QuestionData.objects.all():
        mask_index = qd.question_data["mask_index"]
        if mask_index is None:
            print("refill, mask index error!")
            return
        word = qd.sentence.sentence.split()[mask_index]
        print(f"dodaje synonimy dla slowa: {word}")
        data = []
        saved = 0
        for s in get_synonyms(word):
            print(s)
            synonyms_saved += 1
            data.append({"token": s, "source": "wordnet"})
        qd.question_data["options"].extend(data)
        qd.save()
        questions_saved += 1

    print(f"zapisano {synonyms_saved} synonimy w {questions_saved} pytaniach!")

def get_synset_entries(word):
    """
    Zwraca słownik:
    {
        "word": podane w argumencie słowo,
        "results": lista słowników:
            "word": znacznie slowa, np. kot1, kot2..
            "context_text": połączone w jedno opis, definicja i bogata definicja
    }
    """
    results = []
    lus = wn.find(word)

    for i, lu in enumerate(lus):
        s = lu.synset
        entry = {
            "word": lu.name + str(i),  # np. deska1, kot3 ...
            "context_text": (s.definition or "")
            + (lu.description or "")
            + (lu.rich_description or ""),  # polaczone opisy
        }

        results.append(entry)

    return {"word": word, "results": results}

def wsd_data_for_single_sentence(given_sentence):
    """
    Zwraca słownik:
    "best_overlap_id" -> id najlepszego 
    "entries": entries dla most_ambiguous_homonym,
    "sentence": given_sentence,
    "most_ambiguous_word": most_ambiguous_homonym,
    """
    sentence = set(given_sentence.split())
    most_ambiguous_homonym = None
    most_meanings = 0

    for word in sentence:
        
        # zamiana na formę bazową
        word = get_base_form_and_tag(word)["base_form"]
        
        # usunięcie go jeśli niz nie znaczy
        if word in SKIP_WORDS:
            del word
            continue

        # sprawdzenie czy słowo jest homonimem
        meanings_count = len(get_synset_entries(word)["results"])
        if meanings_count < 2:
            continue

        # szukanie najbardziej wieloznaczeniowego wyrazu
        if meanings_count > most_meanings:
            most_ambiguous_homonym = word
            most_meanings = meanings_count

    print(f'odmieniona forma: {base_form}')
    if most_meanings < 2:
        raise Exception("słabe zdanie, nie ma homonimu")

    biggest_overlap = 0
    biggest_overlap_word = None
    sentence_counter = Counter(sentence)
    entries = []
    best_overlap_id = None  # ktora definicja z kolei ma najwiekszy overlap

    for i, entry in enumerate(get_synset_entries(most_ambiguous_homonym)["results"]):
        option = {"id": i, "entry": entry, "overlap_count": 0}
        context_counter = Counter(entry["context_text"])
        common_counter = context_counter & sentence_counter

        if common_counter:  # jesli są wspólne słowa
            overlap_word, overlap_count = max(
                dict(common_counter).items(), key=itemgetter(1)
            )

            option["overlap_count"] = overlap_count
            option["overlap_word"] = overlap_word

            if overlap_count > biggest_overlap:
                biggest_overlap = overlap_count
                biggest_overlap_word = overlap_word
                best_overlap_id = i
                
        entries.append(option)
        
    
    return {
        "best_overlap_id": best_overlap_id,
        "entries": entries,
        "sentence": given_sentence,
        "most_ambiguous_word": most_ambiguous_homonym,
    }

def create_full_wsd_data():
    created_questions = 0
    created_question_datas = 0
    
    for text in Text.objects.all():
        quiz , created_q = Quiz.objects.get_or_create(text=text)
        quiz_data, created_qd = QuizData.objects.get_or_create(quiz=quiz)
        
        for sentence in text.sentences_without_data:
            
            # tworzenie obiektu QuestionData
            question_data_o = QuestionData()
            question_data_o.sentence = sentence
            question_data_o.quiz_data = quiz_data
            question_data_o.question_data = wsd_data_for_single_sentence(sentence.sentence)
            question_data_o.save()
            
            created_question_datas += 1
            
            # tworzenie obiektu Question
            question = Question()
            question.question_data = question_data_o
            question.question_type = 3 # TODO Question.QuestionType...
            question.save()
            
            created_questions +=1
            
    return print(f'{created_questions=}, {created_question_datas=} ')

def _clean_wsd_context_text(str_to_remove:str):
    q_datas = QuestionData.objects.filter(data__question_type=3)
    for q in q_datas:
        for e in q.question_data['entries']:
            text = e['entry']['context_text'].replace(str_to_remove,'')
            e['entry']['context_text'] = text.strip()
        q.save()
            
            
            
if __name__ == "__main__":
    s = '##K:'
    _clean_wsd_context_text(s)
