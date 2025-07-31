from django.contrib import admin
from .models import Book, WordRating, InsertWord, ChooseWord

# Register your models here.
admin.site.register(Book)
admin.site.register(WordRating)
admin.site.register(InsertWord)
admin.site.register(ChooseWord)
