from django import forms
from django.utils.timezone import datetime, timedelta
from . models import BookReview, BookInstance
 


class BookReviewForm(forms.ModelForm):
    def is_valid(self) -> bool:
        valid = super().is_valid()
        if valid:
            reader = self.cleaned_data.get("reader")
            recent_posts = BookReview.objects.filter(
                reader=reader, 
                created_at__gte=(datetime.utcnow()-timedelta(hours=1))
            )
            if recent_posts:
                return False
        return valid

    class Meta:
        model = BookReview
        fields = ('content', 'book', 'reader', )
        widgets = {
            'book': forms.HiddenInput(),
            'reader': forms.HiddenInput(),
        }

class DateInput(forms.DateInput):
    input_type = 'date'



class BookInstanceForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ('book', 'due_back',)
        widgets = {'due_back': DateInput()}

class BookInstanceUpdateForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ('book', 'due_back',)
        widgets = {'due_back': DateInput(), 'book': forms.HiddenInput()}