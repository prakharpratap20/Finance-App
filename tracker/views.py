from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.conf import settings
from tracker.models import Transaction
from tracker.filters import TransactionFilter
from tracker.forms import TransactionForm
from django_htmx.http import retarget


def index(request):
    """
    This view is used to render the home page of the application.
    """
    return render(request, "tracker/index.html")


@login_required
def transactions_list(request):
    """
    This view is used to render the list of transactions for the authenticated user.
    """
    transaction_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(
            user=request.user).select_related("category")
    )
    paginator = Paginator(transaction_filter.qs, settings.PAGE_SIZE)
    # default to 1 when this view is triggered by a form submission
    transaction_page = paginator.page(1)

    total_income = transaction_filter.qs.get_total_income()
    total_expenses = transaction_filter.qs.get_total_expenses()
    context = {
        "transactions": transaction_page,
        "filter": transaction_filter,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_income": total_income - total_expenses,
    }

    if request.htmx:
        return render(
            request,
            "tracker/partials/transactions-container.html",
            context,
        )

    return render(request, "tracker/transactions-list.html", context)


@login_required
def create_transaction(request):
    """
    This view is used to create a new transaction for the authenticated user.
    """
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            context = {"message": "Transaction was added successfully!"}
            return render(request, "tracker/partials/transaction-success.html", context)
        else:
            context = {"form": form}
            response = render(
                request, "tracker/partials/create-transaction.html", context
            )
            return retarget(response, "#transaction-block")

    context = {"form": TransactionForm()}
    return render(request, "tracker/partials/create-transaction.html", context)


@login_required
def update_transaction(request, pk):
    """
    This view is used to update an existing transaction for the authenticated user.
    """
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            transaction = form.save()
            transaction.user = request.user
            transaction.save()
            context = {"message": "Transaction was updated successfully!"}
            return render(request, "tracker/partials/transaction-success.html", context)
        else:
            context = {
                "form": form,
                "transaction": transaction,
            }
            response = render(
                request, "tracker/partials/update-transaction.html", context
            )
            return retarget(response, "#transaction-block")

    context = {
        "form": TransactionForm(instance=transaction),
        "transaction": transaction,
    }
    return render(request, "tracker/partials/update-transaction.html", context)


@login_required
@require_http_methods(["DELETE"])
def delete_transaction(request, pk):
    """
    This view is used to delete an existing transaction for the authenticated user.
    """
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    transaction.delete()
    context = {
        "message": f"Transaction of {transaction.amount} on {transaction.date} was deleted successfully."
    }
    return render(request, "tracker/partials/transaction-success.html", context)


@login_required
def get_transactions(request):
    """
    This view is used to fetch transactions for the authenticated user.
    """
    # simulate a slow connection
    # import time
    # time.sleep(1)
    page = request.GET.get("page", 1)
    transaction_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(
            user=request.user).select_related("category")
    )
    paginator = Paginator(transaction_filter.qs, settings.PAGE_SIZE)
    context = {
        "transactions": paginator.page(page),
    }

    return render(
        request,
        "tracker/partials/transactions-container.html#transaction_list",
        context
    )
