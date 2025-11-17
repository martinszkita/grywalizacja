from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
from .forms import *


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


def fill_mask_question(request, question_num):
    quiz_data = QuizData.objects.get(quiz__text=request.session["text_id"])
    question_datas = QuestionData.objects.filter(
        quiz_data=quiz_data, data__question_type=Question.QuestionType.FM
    )
    question_count = question_datas.count()

    if question_num > question_count - 1:
        return redirect("guess_replacement_question", question_num=0)

    question_data = question_datas[question_num]
    sentence = question_data.sentence
    choices = question_data.options_json_to_tuple()
    print(choices)
    if isinstance(question_data.question_data, dict): 
        mask_index = question_data.question_data["mask_index"]
    else:
        return HttpResponse(f'question data type: {type(question_data.question_data)}')
    
    masked_sentence = sentence.sentence.split()
    masked_sentence[mask_index] = "_____"
    question = Question.objects.get(question_data=question_data)

    context = {
        "masked_sentence": " ".join(masked_sentence),
        "question_num": question_num + 1,
        "question_count": question_count,
    }

    if request.method == "POST":
        form = FillMaskForm(request.POST, choices=choices, question=question)

        if form.is_valid():
            question_answer = form.save(commit=False)
            question_answer.question = question
            quiz_answer = QuizAnswer.objects.get(id=request.session["quiz_answer_id"])
            question_answer.quiz_answer = quiz_answer
            question_answer.save()
            context["form"] = form

            return redirect("fill_mask_question", question_num=question_num + 1)
        else:
            messages.error(request, "Proszę zaznaczyć odpowiedź!")
            context["form"] = form

            return render(request, "quiz/fill_mask_question.html", context)
    else:
        form = FillMaskForm(choices=choices, question=question)
        context["form"] = form

    return render(request, "quiz/fill_mask_question.html", context)


def guess_replacement_question(request, question_num):
    # TODO zoptymalizowac liczbe kwerend
    quiz_data = QuizData.objects.get(quiz__text=request.session["text_id"])
    question_datas = QuestionData.objects.filter(
        quiz_data=quiz_data, data__question_type=Question.QuestionType.GR
    )
    question_count = question_datas.count()

    if question_num > question_count - 1:
        return redirect("quiz_end")

    question_data = question_datas[question_num]
    question = Question.objects.get(question_data=question_data)
    choices = [
        (q, q.upper()) for q in question.question_data.sentence.sentence.split()
    ] + [question.question_data.options_json_to_tuple]

    form = GuessReplacementForm(
        request.POST or None, question=question, choices=choices
    )

    context = {
        "form": form,
        "question_count": question_count,
        "question_num": question_num,
        "sentence": question_data.sentence.sentence,
    }

    if request.method == "POST":
        if form.is_valid():
            question_answer = form.save(commit=False)
            question_answer.question = question
            quiz_answer = QuizAnswer.objects.get(id=request.session["quiz_answer_id"])
            question_answer.quiz_answer = quiz_answer

            # sprawdzenie czy wybrano slowo jesli zaznaczono TAK
            if (
                form.cleaned_data["chosen_word"] == ""
                and question_answer.answer == "tak"
            ):
                return render(request, "quiz/guess_replacement_question.html", context)

            if isinstance(question_answer.answer, str):
                question_answer.answer = {
                    "is_replacement_answer": question_answer.answer
                }
            question_answer.answer["chosen_word"] = form.cleaned_data["chosen_word"]
            question_answer.save()

        else:
            return render(request, "quiz/guess_replacement_question.html", context)

        return redirect("guess_replacement_question", question_num=question_num + 1)

    return render(request, "quiz/guess_replacement_question.html", context)


def start_quiz(request):
    quiz = Quiz.objects.get(text__id=request.session["text_id"])
    quiz_answer, _ = QuizAnswer.objects.get_or_create(quiz=quiz)

    request.session["quiz_answer_id"] = quiz_answer.id
    request.session["quiz_id"] = quiz.id

    return redirect("fill_mask_question", question_num=0)


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
            return redirect("feedback")
        messages.error(request, "Niepoprawna nazwa użytkownika!")
        return redirect("quiz_end")

    context = {"form": form}
    return render(request, "quiz/quiz_end.html", context)


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