from django import forms

RADIO_CHOICES = (
    ("Value One", "Value One Display"),
    ("Value Two", "Text For Value Two"),
    ("Value Three", "Value Three's Display Text")
)

BOOK_CHOICES = (
    (
        "Non-Fiction", (
            ("1", "Deep Learning with Keras"),
            ("2", "Web Development with Django")
        )
    ),
    (
        "Fiction", (
            ("3", "Brave New World"),
            ("4", "The Great Gatsby")
        )
    )
)


class ExampleForm(forms.Form):
    text_input = forms.CharField()
    password_input = forms.CharField(widget=forms.PasswordInput)
    checkbox_on = forms.BooleanField()
    radio_input = forms.ChoiceField(choices=RADIO_CHOICES, widget=forms.RadioSelect)
    favorite_book = forms.ChoiceField(choices=BOOK_CHOICES)
    books_you_own = forms.MultipleChoiceField(choices=BOOK_CHOICES)
    text_area = forms.CharField(widget=forms.Textarea)
    integer_input = forms.IntegerField()
    float_input = forms.FloatField()
    decimal_input = forms.DecimalField(max_digits=3)
    email_input = forms.EmailField()
    date_input = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    hidden_input = forms.CharField(widget=forms.HiddenInput, initial="Hidden Value")
