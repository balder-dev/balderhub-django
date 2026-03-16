from django.contrib import admin

from .models import Author, Category, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'date_of_birth', 'date_of_death']
    search_fields = ['first_name', 'last_name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'publication_date', 'price']
    list_filter = ['categories', 'author', 'publication_date']
    search_fields = ['title', 'isbn', 'author__first_name', 'author__last_name']
    filter_horizontal = ['categories']
