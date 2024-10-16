from django.urls import path
from .api import views as booksApiViews

urlpatterns = [
    path('books/', booksApiViews.BooksViews.as_view(), name="booksViews"),
    path('books/<int:id>', booksApiViews.BooksViews.as_view(), name='booksViewsArgs'),
]