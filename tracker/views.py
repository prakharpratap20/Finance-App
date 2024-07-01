from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tracker.models import Transaction
from tracker.filters import TransactionFilter


def index(request):
    return render(request, "tracker/index.html")


@login_required
def transactions_list(request):
    transaction_filter = TransactionFilter(
        request.GET, queryset=Transaction.objects.filter(user=request.user)
    )
    context = {"filter": transaction_filter}
    return render(request, "tracker/transactions-list.html", context)
