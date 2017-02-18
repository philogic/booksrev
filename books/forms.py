from django import forms


class ReviewForm(forms.Form):
    """
    Book review form.
    """
    is_favourite = forms.BooleanField(
        label="Favourite?",
        help_text="In your top 20 books of all time?",
        required=False,
    )
    review = forms.CharField(
        widget=forms.Textarea,
        min_length=350,
        error_messages={
            'required': "Please, enter your review",
            'min_length': "Please write at least 350 chracters (You have written % (show_value)s)"
        }
    )