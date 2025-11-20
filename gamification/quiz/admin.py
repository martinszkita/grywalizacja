from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *


@admin.register(QuestionData)
class QuestionDataAdmin(admin.ModelAdmin):
    class TextListFilter(admin.SimpleListFilter):
        title = "text title"
        parameter_name = "text__title"

        def lookups(self, request, model_admin):
            text_titles = [(text.title, text.title) for text in Text.objects.all()]
            return text_titles

        def queryset(self, request, queryset):
            value = self.value()

            if value:
                return queryset.filter(sentence__text__title=value)
            return queryset.all()

    class QuestionTypeFilter(admin.SimpleListFilter):
        title = "question type"
        parameter_name = "question_type"

        def lookups(self, request, model_admin):
            return [(qt.label, qt.label) for qt in Question.QuestionType]

        def queryset(self, request, queryset):
            value = self.value()

            if value is None:
                return queryset.all()

            value_int = Question.QuestionType.from_label(value)

            return queryset.filter(data__question_type=value_int)

    list_display = [
        "id",
        "text",
        "question_type",
        "sentence",
    ]
    list_filter = [TextListFilter, QuestionTypeFilter]
    readonly_fields = ["id", "sentence", "mask_str", "question_data"]
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
        "data",
    ]
    list_filter = ["has_data", "text"]

@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    class SentenceInline(admin.TabularInline):
        model = Sentence
        extra = 0
        readonly_fields = ['id','sentence', 'has_data']

    list_display = ['id', 'title', 'sentences_count']
    readonly_fields = ['id', 'title', 'sentences_count']
    fields = ['description', 'image', 'sentences_count']
    inlines = [SentenceInline]
    
admin.site.register(Quiz)
