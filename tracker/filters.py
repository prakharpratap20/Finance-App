from django import forms
# from django.db.models import query
import django_filters
from tracker.models import Transaction, Category


class TransactionFilter(django_filters.FilterSet):
    """
    This class is a filter for the Transaction model.
    It allows filtering transactions by type, date, and category.
    """
    transaction_type = django_filters.ChoiceFilter(
        choices=Transaction.TRANSACTION_TYPE_CHOICES,
        field_name="type",
        lookup_expr="iexact",
        empty_label="Any",
    )
    start_date = django_filters.DateFilter(
        field_name="date",
        lookup_expr="gte",
        label="Date From",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    end_date = django_filters.DateFilter(
        field_name="date",
        lookup_expr="lte",
        label="Date To",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Transaction
        fields = ("transaction_type", "start_date", "end_date", "category")
