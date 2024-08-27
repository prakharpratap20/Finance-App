from django import forms
from tracker.models import Transaction, Category


class TransactionForm(forms.ModelForm):
    """
    Form for creating a new transaction.
    It allows the user to select the type of transaction (income or expense),
    the amount, the date and the category of the transaction.
    """
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.RadioSelect(),
    )

    def clean_amount(self):
        """
        Custom validation for the amount field.
        """
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise forms.ValidationError("Amount must be a positive number")
        return amount

    class Meta:
        model = Transaction
        fields = (
            "type",
            "amount",
            "date",
            "category",
        )
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }
