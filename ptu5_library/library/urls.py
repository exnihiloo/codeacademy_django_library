from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('authors/', views.authors, name = 'authors'),
    path('author/<int:author_id>', views.author, name = 'author'),
    path('books/', views.BookListView.as_view(), name = 'books'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name = 'book'),
    path('my_books/', views.UserBookListView.as_view(), name = 'user_books'),
    path('borrow_new_book/', views.UserBookInstanceCreateView.as_view(), name = 'user_bookinstance_create'),
    path('take_reserved_book/<int:pk>/', views.UserBookInstanceUpdateView.as_view(), name = 'user_bookinstance_update'),
    path('return_book/<int:pk>/', views.UserBookInstanceDeleteView.as_view(), name = 'user_bookinstance_delete'),
    # pk yra primary key
]