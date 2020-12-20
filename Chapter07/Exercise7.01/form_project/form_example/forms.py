from django import forms
from django.core.exceptions import ValidationError


def validate_email_domain(value):
    if value.split("@")[-1].lower() != "example.com":
        raise ValidationError("The email address must be on the domain example.com.")


class OrderForm(forms.Form):
    magazine_count = forms.IntegerField(min_value=0, max_value=80)
    book_count = forms.IntegerField(min_value=0, max_value=50)
    send_confirmation = forms.BooleanField(required=False)
    email = forms.EmailField(required=False, validators=[validate_email_domain])

    def clean_email(self):
        return self.cleaned_data['email'].lower()

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["send_confirmation"] and not cleaned_data.get("email"):
            self.add_error("email", "Please enter an email address to receive the confirmation message.")
        elif cleaned_data.get("email") and not cleaned_data["send_confirmation"]:
            self.add_error("send_confirmation", "Please check this if you want to receive a confirmation email.")

        item_total = cleaned_data.get("magazine_count", 0) + cleaned_data.get("book_count", 0)
        if item_total > 100:
            self.add_error(None, "The total number of items must be 100 or less.")
