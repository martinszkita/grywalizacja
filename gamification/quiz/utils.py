# import random
# from transformers import pipeline
# from .models import *
import morfeusz2
import plwordnet
import pickle

DATA_PATH = "/home/marcin/grywalizacja/gamification/quiz/data/"
SENTENCES_PER_QUESTION_TYPE = 20
FILL_MASK_TOP_K = 5
WHICH_BEST_FILL_MASK_ANSWER = (
    3  # ktora najlespza z kolei opcja do wybrania z fill_mask()
)


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


def create_fill_mask_data():
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
            words[mask_index] = "<mask>"
            masked_sentence = " ".join(words)

            results = fill_mask(masked_sentence, top_k=FILL_MASK_TOP_K)
            options = [{"mask_index": mask_index}] + [
                {"token": r["token_str"], "score": round(r["score"], 4)}
                for r in results
            ]

            quiz, _ = Quiz.objects.get_or_create(text=text)
            quiz_data, _ = QuizData.objects.get_or_create(quiz=quiz)

            question_data, created = QuestionData.objects.get_or_create(
                sentence=sentence, defaults={"quiz_data": quiz_data, "options": options}
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
    texts = Text.objects.all()

    for text in texts:
        sentences_without_data = Sentence.objects.filter(text=text, has_data=False)
        quiz, _ = Quiz.objects.get_or_create(text=text)
        quiz_data, _ = QuizData.objects.get_or_create(quiz=quiz)

        for sentence in sentences_without_data:
            question_data = QuestionData()
            question_data.quiz_data = quiz_data
            question_data.sentence = sentence

            # przygotowanie options:JSON
            is_replacement = random.choice([True, False])
            options = {}

            options["is_replacement"] = is_replacement

            if is_replacement:
                sentene_list = sentence.sentence.split()
                s_len = len(sentene_list)
                replacement_index = random.randint(0, s_len - 1)
                sentene_list[replacement_index] = "<mask>"
                result = fill_mask(" ".join(sentene_list), top_k=FILL_MASK_TOP_K)[
                    WHICH_BEST_FILL_MASK_ANSWER
                ]
                replacement_str = result["token_str"]
                replacement_score = result["score"]

                options["replacement_index"] = replacement_index
                options["replacement_str"] = replacement_str
                options["replacement_score"] = replacement_score
                options["which_best"] = WHICH_BEST_FILL_MASK_ANSWER

            question_data.options = options
            question_data.save()

            print(
                f" sentence_id: {sentence.id} dotaje question_data_id:{question_data.id}"
            )

            question = Question()
            question.question_data = question_data
            question.question_type = Question.QuestionType.GR
            question.save()

            sentence.save()
            print(f"po sentence.save() has_data: {sentence.has_data}")


def get_base_form_and_tag(morf, word):
    # morf = morfeusz2.Morfeusz()
    analyses = morf.analyse(word)

    if not analyses:
        return {"base_form": word, "form_tag": None}

    # wybieramy pierwszą interpretację
    _, _, interp = analyses[0]

    return {"base_form": interp[1].split(":")[0], "form_tag": interp[2]}


def get_synset_words(word):
    with open("/home/marcin/grywalizacja/wordnet.pkl", "rb") as f:
        wn = pickle.load(f)
        word_lus = wn.find(word)
        words = []

        for lu in word_lus:
            names = [item.name for item in lu.synset.lexical_units if item.name.find(' ') < 0] # odrzucamy wielowyrazowe
            words.extend(names)

    return list(set(words))  # usuwamy duplikaty


def generate_given_form(morf, word, tag):
    resolver = morf._morfeusz_obj.getIdResolver()
    tag_id = resolver.getTagId(tag)
    
    for orth, lemma, tag, name, labels in morf.generate(word, tag_id):
        return orth

def get_synonyms(word='grała'):
    base_form = get_base_form_and_tag(morf, word)["base_form"].split(":")[0]
    base_form_tag = get_base_form_and_tag(morf, word)["form_tag"]
    synset = get_synset_words(base_form)
    new_forms = set()

    for s in synset:
        new_form = generate_given_form(morf, s, base_form_tag)
        if new_form is None:
            continue
        new_forms.add(new_form)
    
    return new_forms


if __name__ == "__main__":
    morf = morfeusz2.Morfeusz()
    print(get_synonyms('chłopakom'))
        
