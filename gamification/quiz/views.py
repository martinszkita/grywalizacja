from typing import Optional

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
from .forms import *


QUESTION_ORDER = [
    ("fill-mask", Question.QuestionType.FM, FillMaskForm, "quiz/fill_mask_question.html"),
    (
        "guess-replacement",
        Question.QuestionType.GR,
        GuessReplacementForm,
        "quiz/guess_replacement_question.html",
    ),
    ("wsd", Question.QuestionType.WSD, WsdQuestionForm, "quiz/wsd_question.html"),
]
QUESTION_PER_SECTION = 20
QUESTION_SECTION_MAP = {
    slug: {
        "question_type": question_type,
        "form": form,
        "template": template,
        "slug": slug,
    }
    for slug, question_type, form, template in QUESTION_ORDER
}


# Create your views here.
def quiz(request):
    return redirect("quiz_info")


def quiz_info(request):
    return render(request, "quiz/quiz_info.html", {})


def topic_choice(request):
    texts = Text.objects.all()
    chosen_topic = request.GET.get("topic")

    if chosen_topic:
        text = Text.objects.get(title=chosen_topic)
        text_id = text.id
        request.session["text_id"] = text_id

        return redirect("start_quiz")

    return render(request, "quiz/topic_choice.html", {"texts": texts})


def start_quiz(request):
    text_id = request.session.get("text_id")
    if not text_id:
        return redirect("topic_choice")

    quiz = Quiz.objects.get(text__id=text_id)
    QuizData.objects.get_or_create(quiz=quiz)
    quiz_answer = QuizAnswer.objects.create(quiz=quiz)

    request.session["quiz_answer_id"] = quiz_answer.id
    request.session["quiz_id"] = quiz.id

    return redirect("question", section=QUESTION_ORDER[0][0], question_num=0)


def _get_next_section(current_section: str) -> Optional[str]:
    for index, (slug, *_rest) in enumerate(QUESTION_ORDER):
        if slug == current_section and index + 1 < len(QUESTION_ORDER):
            return QUESTION_ORDER[index + 1][0]
    return None


def _get_quiz_data_or_redirect(request):
    text_id = request.session.get("text_id")
    if not text_id:
        return None, redirect("topic_choice")

    quiz_data = QuizData.objects.filter(quiz__text_id=text_id).first()
    if not quiz_data:
        return None, redirect("topic_choice")

    return quiz_data, None


def question(request, section: str, question_num: int):
    section_config = QUESTION_SECTION_MAP.get(section)
    if not section_config:
        return redirect("topic_choice")

    quiz_data, redirect_response = _get_quiz_data_or_redirect(request)
    if redirect_response:
        return redirect_response

    question_datas = list(
        QuestionData.objects.filter(
            quiz_data=quiz_data, data__question_type=section_config["question_type"]
        )
        .select_related("sentence")
        .order_by("id")[:QUESTION_PER_SECTION]
    )
    question_count = len(question_datas)

    if question_count == 0:
        next_section = _get_next_section(section)
        if next_section:
            return redirect("question", section=next_section, question_num=0)
        return redirect("quiz_end")

    if question_num > question_count - 1:
        next_section = _get_next_section(section)
        if next_section:
            return redirect("question", section=next_section, question_num=0)
        return redirect("quiz_end")

    question_data = question_datas[question_num]
    question = Question.objects.get(question_data=question_data)
    base_context = {
        "question_num": question_num + 1,
        "question_count": question_count,
        "section": section,
    }

    try:
        choices = question_data.options_json_to_tuple()
    except KeyError:
        choices = []

    if section == "fill-mask":
        return _handle_fill_mask_question(
            request=request,
            question=question,
            question_data=question_data,
            question_num=question_num,
            template=section_config["template"],
            choices=choices,
            base_context=base_context,
        )

    if section == "guess-replacement":
        return _handle_guess_replacement_question(
            request=request,
            question=question,
            question_data=question_data,
            question_num=question_num,
            template=section_config["template"],
            base_context=base_context,
        )

    return _handle_wsd_question(
        request=request,
        question=question,
        question_data=question_data,
        question_num=question_num,
        template=section_config["template"],
        base_context=base_context,
        choices=choices,
    )


def _attach_answer_to_quiz(question_answer, question, quiz_answer_id):
    question_answer.question = question
    quiz_answer = QuizAnswer.objects.get(id=quiz_answer_id)
    question_answer.quiz_answer = quiz_answer
    question_answer.save()


def _handle_fill_mask_question(
    request,
    question,
    question_data,
    question_num,
    template,
    base_context,
    choices,
):
    quiz_answer_id = request.session.get("quiz_answer_id")
    if not quiz_answer_id:
        return redirect("start_quiz")

    question_payload = (
        question_data.question_data if isinstance(question_data.question_data, dict) else {}
    )
    mask_index = question_payload.get("mask_index")
    masked_sentence = question_data.sentence.sentence.split()
    if mask_index is not None and mask_index < len(masked_sentence):
        masked_sentence[mask_index] = "_____"

    context = {
        **base_context,
        "masked_sentence": " ".join(masked_sentence),
    }
    form = FillMaskForm(request.POST or None, choices=choices, question=question)
    context["form"] = form

    if request.method == "POST":
        if form.is_valid():
            question_answer = form.save(commit=False)
            _attach_answer_to_quiz(question_answer, question, quiz_answer_id)
            return redirect(
                "question", section=QUESTION_ORDER[0][0], question_num=question_num + 1
            )
        messages.error(request, "Proszę zaznaczyć odpowiedź!")

    return render(request, template, context)


def _handle_guess_replacement_question(
    request,
    question,
    question_data,
    question_num,
    template,
    base_context,
):
    quiz_answer_id = request.session.get("quiz_answer_id")
    if not quiz_answer_id:
        return redirect("start_quiz")

    choices = [(word, word.upper()) for word in question_data.sentence.sentence.split()]
    form = GuessReplacementForm(
        request.POST or None, question=question, choices=choices
    )

    context = {**base_context, "form": form, "sentence": question_data.sentence.sentence}

    if request.method == "POST":
        if form.is_valid():
            if form.cleaned_data["answer"] == "tak" and not form.cleaned_data["chosen_word"]:
                messages.error(request, "Wskaż słowo, które zostało zamienione.")
                return render(request, template, context)

            question_answer = form.save(commit=False)
            current_answer = question_answer.answer
            if isinstance(current_answer, str):
                current_answer = {"is_replacement_answer": current_answer}
            current_answer = current_answer or {}
            current_answer["chosen_word"] = form.cleaned_data.get("chosen_word", "")
            question_answer.answer = current_answer

            _attach_answer_to_quiz(question_answer, question, quiz_answer_id)
            return redirect(
                "question",
                section="guess-replacement",
                question_num=question_num + 1,
            )
        messages.error(request, "Proszę zaznaczyć odpowiedź!")

    return render(request, template, context)


def _handle_wsd_question(
    request,
    question,
    question_data,
    question_num,
    template,
    base_context,
    choices,
):
    quiz_answer_id = request.session.get("quiz_answer_id")
    if not quiz_answer_id:
        return redirect("start_quiz")

    question_payload = (
        question_data.question_data if isinstance(question_data.question_data, dict) else {}
    )
    target_word = question_payload.get("target_word")

    context = {
        **base_context,
        "sentence": question_data.sentence.sentence,
        "target_word": target_word,
    }

    form = WsdQuestionForm(request.POST or None, choices=choices, question=question)
    context["form"] = form

    if request.method == "POST":
        if form.is_valid():
            question_answer = form.save(commit=False)
            _attach_answer_to_quiz(question_answer, question, quiz_answer_id)
            return redirect("question", section="wsd", question_num=question_num + 1)
        messages.error(request, "Proszę zaznaczyć odpowiedź!")

    return render(request, template, context)


def quiz_end(request):
    form = UsernameForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["username"]
            if not username:
                messages.error(request, "Proszę wpisać swój nick!")
                return redirect("quiz_end")
            quiz_answer_id = request.session["quiz_answer_id"]
            quiz_answer = QuizAnswer.objects.get(id=quiz_answer_id)
            quiz_answer.username = username
            quiz_answer.save()
            request.session["username"] = username
            return redirect("summary")
        messages.error(request, "Niepoprawna nazwa użytkownika!")
        return redirect("quiz_end")

    context = {"form": form}
    return render(request, "quiz/quiz_end.html", context)


def summary(request):
    quiz_answer_id = request.session.get("quiz_answer_id")
    if not quiz_answer_id:
        return redirect("topic_choice")

    quiz_answer = QuizAnswer.objects.select_related("quiz__text").prefetch_related(
        "answers__question"
    ).get(id=quiz_answer_id)

    question_counts = {
        "fill_mask": quiz_answer.answers.filter(
            question__question_type=Question.QuestionType.FM
        ).count(),
        "guess_replacement": quiz_answer.answers.filter(
            question__question_type=Question.QuestionType.GR
        ).count(),
        "wsd": quiz_answer.answers.filter(
            question__question_type=Question.QuestionType.WSD
        ).count(),
    }

    context = {
        "quiz_answer": quiz_answer,
        "question_counts": question_counts,
        "total_answered": sum(question_counts.values()),
    }

    return render(request, "quiz/summary.html", context)


def feedback(request):
    if request.session["quiz_answer_id"]:
        quiz_answer_id = request.session["quiz_answer_id"]
    else:
        return HttpResponse("quiz_answer_id error while summary!")

    quiz_answer = QuizAnswer.objects.get(id=quiz_answer_id)
    form = UserFeedbackForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user_feedback = form.cleaned_data["user_feedback"]
            user_comment = form.cleaned_data["user_comment"]

            if user_comment:
                quiz_answer.user_comment = user_comment

            if user_feedback:
                quiz_answer.user_feedback = user_feedback

            quiz_answer.save()
            return redirect("quiz")

        messages.error(request, form.errors.as_text())
        return redirect("feedback")

    context = {"form": form}

    return render(request, "quiz/feedback.html", context)

def quiz_stats(request):
    pass