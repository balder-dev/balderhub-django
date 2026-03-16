from django.db import models


class Author(models.Model):
    """Model representing a book author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)
    biography = models.TextField(blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Category(models.Model):
    """Model representing a book category/genre."""
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Book(models.Model):
    """Model representing a book."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name='books')
    categories = models.ManyToManyField(Category, related_name='books', blank=True)
    isbn = models.CharField('ISBN', max_length=13, unique=True)
    summary = models.TextField(blank=True)
    publication_date = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pages = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
