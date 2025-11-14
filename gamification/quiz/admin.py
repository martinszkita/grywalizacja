from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *


@admin.register(QuestionData)
class QuestionDataAdmin(admin.ModelAdmin):
    class TextListFilter(admin.SimpleListFilter):
        title = "text title"
        parameter_name = "text title parameter"

        def lookups(self, request, model_admin):
            return [("delfiny", "DELFINY"),
                    ("maroko", "MAROKO"),
                    ("sieci_neuronowe", 'SIECI_NEURONOWE')]
        
        def queryset(self, request, queryset):
            value = self.value()
            if value == "delfiny":
                return queryset.filter(sentence__text__title="delfiny")
            if value == "maroko":
                return queryset.filter(sentence__text__title="maroko")
            if value == "sieci_neuronowe":
                return queryset.filter(sentence__text__title="sieci_neuronowe")

            return queryset
        
    list_display = [
        "id",
        "text",
        "question_type",
        "sentence",
    ]
    list_filter = [
        TextListFilter,
    ]
    readonly_fields = ["id", "sentence", "mask_str", "options"]
    exclude = [
        "quiz_data",
    ]

    def sentence(self, question_data_object):
        return question_data_object.sentence.sentence

    def mask_str(self, question_data_object):
        if self.question_type != "FM":
            return "-"

        index = question_data_object.options[0]["mask_index"]
        return question_data_object.sentence.sentence.split()[index]

    def options(self, question_data_object):
        return question_data_object.question_data["options"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "text",
        "question_type",
        "sentence",
    ]
    list_filter = [
        "question_type",
    ]
    readonly_fields = ["id", "text", "question_type", "sentence"]

    def sentence(self, question_object):
        return question_object.question_data.sentence.sentence

    def text(self, question_object):
        return question_object.question_data.sentence.text.title


@admin.register(QuizData)
class QuizDataAdmin(admin.ModelAdmin):
    list_display = ["text_title", "question_number"]
    readonly_fields = [
        "text_title",
    ]
    exclude = [
        "quiz",
    ]

    def text_title(self, quiz_data_object):
        return quiz_data_object.quiz.text.title

    def question_number(self, quiz_data_object):
        return QuestionData.objects.filter(quiz_data=quiz_data_object).count()


@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "date",
        "text_title",
        "answered_questions_num",
    ]  # dodac username
    readonly_fields = [
        "id",
        "date",
        "text_title",
        "answered_questions_num",
        "user_feedback",
        "user_comment",
    ]
    exclude = [
        "quiz",
    ]

    def text_title(self, quiz_answer_obj):
        return quiz_answer_obj.quiz.text.title


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ["id", "date", "text_title", "username"]

    def text_title(self, question_answer_obj):
        return question_answer_obj.quiz_answer.quiz.text.title

    def username(self, question_answer_obj):
        return question_answer_obj.quiz_answer.username

    def date(self, question_answer_obj):
        return question_answer_obj.quiz_answer.date


@admin.register(Sentence)
class SentenceAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "has_data",
        "text",
        "sentence",
    ]
    readonly_fields = [
        "sentence",
        "has_data",
        "text",
    ]
    list_filter = ["has_data", "text"]


admin.site.register(Text)
admin.site.register(Quiz)
