from django.db import models
from django.utils.html import format_html
from django.urls import reverse
import uuid
from django.contrib.auth import get_user_model
from django.utils.timezone import datetime
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField

# Create your models here.
class Genre(models.Model):
    name = models.CharField(_('name'), max_length = 200, help_text = _("Enter name of book genre"))

    def __str__(self):
        return self.name

    def link_filtered_books(self) -> str:
        link = reverse('books') + '?genre_id='+str(self.id)
        return format_html('<a class="genre" href="{link}">{name}</a>', link = link, name = self.name)

    class Meta:
        ordering = ['name']
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

# models.Model  django funkcija, models importuoja Model, panasiai kaip sqlalchemy Base
class Author(models.Model):
    first_name = models.CharField(_('first name'), max_length = 50)
    last_name = models.CharField(_('last name'), max_length = 150)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def display_books(self) -> str:
        return ", ".join(book.title for book in self.books.all())
    display_books.short_description = _('books')

    def link(self) -> str:
        link = reverse('author', kwargs={'author_id' : self.id})
        return format_html('<a href="{link}">{author}</a>', link = link, author = self.__str__())

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = _('author')
        verbose_name_plural = _('authors')

# charfield yra duomenu bazes efektyvus duomenu laukas, lengvai rusiuojasi, indeksuojasi
# textfield yra sunkus duomenu laukas, neturi limito su length
class Book(models.Model):
    title = models.CharField(_('title'), max_length = 255)
    summary = HTMLField(_('summary'))
    isbn = models.CharField('ISBN', max_length=13, null=True, blank=True,
        help_text=_('<a href="https://www.isbn-international.org/content/what-isbn" target="_blank">ISBN code</a> consisting of 13 symbols'))
    # jei foreign key butu su objektu, kuris zemiau sios klases, reiktu deti pavaidnima i kabutes, jei authior butu zemiau tai butu "Author"
    # protect neleis istrinti autoriaus, jei jis turi knygas
    # set_null jei istirnsim autoriu, prie knygu rodys autoriu null
    # cascade jei istrinsime autoriu istrins ir jo visas knygas
    author = models.ForeignKey(Author, on_delete = models.SET_NULL, null = True, blank = True, related_name = 'books',)
    genre = models.ManyToManyField(Genre, help_text = _('Choose genre(s) for this book'), verbose_name = _('genre(s)'))
    cover = models.ImageField(_("cover"), upload_to = 'covers', blank = True, null = True)

    def __str__(self):
        return f"{self.author} - {self.title}"

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    display_genre.short_description = _('genre(s)')

    class Meta:
        verbose_name = _('book')
        verbose_name_plural = _('books')

    # reverse suformuoja adresa

    # def author_link(self) -> str:
    #     link = reverse('author', kwargs = {'author_id' : self.author.id})
    #     return format_html('<a href="{link}">{author}</a>', link = link, author = self.author)

    # kai sukuriam modeli radom python manage.py makemigrations
    # tada python manage.py migrate

# pirmos reiksmes kabutese yra verbose_name jei nenurodome verbose_name, tai turime juos pirmus nurodyti
# jei bus foreign key tai pirmas turi eiti klases objektas

class BookInstance(models.Model):
    unique_id = models.UUIDField(_('unique ID'), default = uuid.uuid4, editable = False)
    book = models.ForeignKey(Book, verbose_name = (''), on_delete = models.CASCADE)
    due_back = models.DateField(_('due back'), null = True, blank = True)

    LOAN_STATUS = (
        ('m', _('managed')),
        ('t', _('taken')),
        ('a', _('available')),
        ('r', _('reserved'))
    )

    status = models.CharField(
        _('status'), 
        max_length = 1, 
        choices = LOAN_STATUS, 
        default = 'm')

    reader = models.ForeignKey(
        get_user_model(), 
        verbose_name=_("reader"), 
        on_delete=models.SET_NULL,
        null = True, blank = True,
        related_name='taken_books'
    )

    
    @property
    def is_overdue(self):
        if self.due_back and self.due_back < datetime.date(datetime.now()):
            return True
        return False

    def __str__(self) -> str:
        return f"{self.unique_id} : {self.book.title}"

    class Meta:
        ordering = ['due_back']
        verbose_name = _('book instance')
        verbose_name_plural = _('book instances')

class BookReview(models.Model):
    book = models.ForeignKey(
        Book,
        verbose_name=_('book'),
        on_delete=models.CASCADE, 
        related_name='reviews'
    )
    reader = models.ForeignKey(
        get_user_model(), 
        verbose_name=_('reader'), 
        on_delete=models.CASCADE, 
        related_name='book_reviews'
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    content = models.TextField(_("content"), max_length=2000)


    def __str__(self):
        return f"{self.reader} on {self.book} at {self.created_at}"

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('book review')
        verbose_name_plural = _('book reviews')