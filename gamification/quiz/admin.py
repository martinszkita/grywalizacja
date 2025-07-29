from django.contrib import admin
from .models import Book, WordRating, InsertWord
# Register your models here.
admin.site.register(Book)
admin.site.register(WordRating)
admin.site.register(InsertWord)