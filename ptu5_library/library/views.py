from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator


from . models import Genre, Author, Book, BookInstance
# Create your views here.

def index(request):
    # return HttpResponse("Sveiki atvykę!")
    book_count = Book.objects.count()
    book_instance_count = BookInstance.objects.count()
    book_instance_available_count = BookInstance.objects.filter(status = 'a').count()
    author_count = Author.objects.count()


    context = {
        'book_count' : book_count,
        'book_instance_count' : book_instance_count,
        'book_instance_available_count' : book_instance_available_count,
        'author_count' : author_count,
        'genre_count': Genre.objects.count(),
    }

    return render(request, 'library/index.html', context) 
    # jei sablonas skirtas appsui tai ji idedame i appso folderi

# funkciniai views.
# autoriu funkcija
def authors(request):
    paginator = Paginator(Author.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_authors = paginator.get_page(page_number)
    return render(request, 'library/authors.html', {'authors' : paged_authors})

# author detail funkcija
def author(request, author_id):
    return render(request, 'library/author.html', {'author' : get_object_or_404(Author, id=author_id)})

# class based view

class BookListView(ListView):
    model = Book
    paginate_by = 2
    template_name = 'library/book_list.html'

    #is get kolekcijos argumentu pabandysime gauti zanro id
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(Q(title__icontains = query) | Q(summary__icontains = query))
        genre_id = self.request.GET.get('genre_id')
        if genre_id:
            queryset = queryset.filter(genre__id = genre_id)
        return queryset

        # genre__id du underscore nes yra many to many sarysis, kreipiames i zanro lentele per tarpine lentele
        # del to 2 udnerscore


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['books_count'] = Book.objects.count()
        # antras budas skaiciuoti, ji labiau naudoja djangistai
        context['books_count'] = self.get_queryset().count()
        genre_id = self.request.GET.get('genre_id')
        context['genres'] = Genre.objects.all()
        if genre_id:
            context['genre'] = get_object_or_404(Genre, id = genre_id)
        return context

class BookDetailView(DetailView):
    model = Book
    template_name = 'library/book_detail.html'


# def search(request):
#     query = request.GET.get('query')
#     search_results = Book.objects.filter(Q(title__icontains = query) | Q(summary__icontains = query))
#     return render(request, 'library/search.html', {'books' : search_results, 'query' : query})