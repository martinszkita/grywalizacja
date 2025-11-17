import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gamification.settings")
django.setup()

import random
from transformers import pipeline
import morfeusz2
import plwordnet
import pickle
from .models import *

DATA_PATH = "/home/marcin/grywalizacja/gamification/quiz/data/"
SENTENCES_PER_QUESTION_TYPE = 20
FILL_MASK_TOP_K = 5
WHICH_BEST_FILL_MASK_ANSWER = (
    3  # ktora najlespza z kolei opcja do wybrania z fill_mask()
)

morf = morfeusz2.Morfeusz()


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
    for text in Text.objects.all():
        sentences_without_data = Sentence.objects.filter(text=text, has_data=False)
        if sentences_without_data.count() < SENTENCES_PER_QUESTION_TYPE:
            raise Exception("nie ma 20 zdan bez danych dla tekstu: ", text.title)

        quiz, _ = Quiz.objects.get_or_create(text=text)
        quiz_data, _ = QuizData.objects.get_or_create(quiz=quiz)

        for sentence in sentences_without_data[:SENTENCES_PER_QUESTION_TYPE]:
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

            print(f" sentence_id: {sentence.id} dostaje:{question_data}")

            question = Question()
            question.question_data = question_data_o
            question.question_type = Question.QuestionType.GR
            question.save()
            sentence.save()


def get_synset_words(word):
    with open("/home/marcin/grywalizacja/wordnet.pkl", "rb") as f:
        wn = pickle.load(f)
        word_lus = wn.find(word)
        words = []

        for lu in word_lus:
            names = [
                item.name for item in lu.synset.lexical_units if item.name.find(" ") < 0
            ]  # odrzucamy wielowyrazowe
            words.extend(names)

    return list(set(words))  # usuwamy duplikaty


def get_synonyms(word="grała"):
    def generate_given_form(word, tag):
        resolver = morf._morfeusz_obj.getIdResolver()
        tag_id = resolver.getTagId(tag)

        for orth, lemma, tag, name, labels in morf.generate(word, tag_id):
            return orth

    def get_base_form_and_tag(word):
        # morf = morfeusz2.Morfeusz()
        analyses = morf.analyse(word)

        if not analyses:
            return {"base_form": word, "form_tag": None}

        # wybieramy pierwszą interpretację
        _, _, interp = analyses[0]

        return {"base_form": interp[1].split(":")[0], "form_tag": interp[2]}

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


if __name__ == "__main__":
    # refill_fill_mask_data_wordnet()
    create_guess_replacement_data()
