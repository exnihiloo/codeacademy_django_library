from django.db import models
import uuid

# Create your models here.
class Genre(models.Model):
    name = models.CharField('name', max_length = 200, help_text = "Enter name of book genre")

    def __str__(self):
        return self.name

# models.Model  django funkcija, models importuoja Model, panasiai kaip sqlalchemy Base
class Author(models.Model):
    first_name = models.CharField('first name', max_length = 50)
    last_name = models.CharField('last name', max_length = 150)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['last_name', 'first_name']

# charfield yra duomenu bazes efektyvus duomenu laukas, lengvai rusiuojasi, indeksuojasi
# textfield yra sunkus duomenu laukas, neturi limito su length
class Book(models.Model):
    title = models.CharField('title', max_length = 255)
    summary = models.TextField('summary')
    isbn = models.CharField('ISBN', max_length=13, null=True, blank=True,
        help_text='<a href="https://www.isbn-international.org/content/what-isbn" target="_blank">ISBN code</a> consisting of 13 symbols')
    # jei foreign key butu su objektu, kuris zemiau sios klases, reiktu deti pavaidnima i kabutes, jei authior butu zemiau tai butu "Author"
    # protect neleis istrinti autoriaus, jei jis turi knygas
    # set_null jei istirnsim autoriu, prie knygu rodys autoriu null
    # cascade jei istrinsime autoriu istrins ir jo visas knygas
    author = models.ForeignKey(Author, on_delete = models.SET_NULL, null = True, blank = True)
    genre = models.ManyToManyField(Genre, help_text = 'Choose genre(s) for this book', verbose_name = 'genre(s)')

    def __str__(self):
        return f"{self.author} - {self.title}"

    # kai sukuriam modeli radom python manage.py makemigrations
    # tada python manage.py migrate

class BookInstance(models.Model):
    unique_id = models.UUIDField('unique ID', default = uuid.uuid4, editable = False)
    book = models.ForeignKey(Book, verbose_name = (''), on_delete = models.CASCADE)
    due_back = models.DateField('due back', null = True, blank = True)

    LOAN_STATUS = (
        ('m', 'managed'),
        ('t', 'taken'),
        ('a', 'available'),
        ('r', 'reserved')
    )

    status = models.CharField(
        'status', 
        max_length = 1, 
        choices = LOAN_STATUS, 
        default = 'm')

    price = models.DecimalField('price', max_digits = 18, decimal_places = 2) # decimal_places, skaicius po kablelio

    def __str__(self):
        return f"{self.unique_id} : {self.book.title}"

    class Meta:
        ordering = ['due_back']