from django import forms


class AddCommentForm(forms.Form):
    message = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Add a Comment"}), required=True
    )

