from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import TransactionQuerySet


class User(AbstractUser):
    pass


class Category(models.Model):
    """
    Category model for storing the transaction categories with the following fields:
    - name: CharField for storing the category name
    """
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return f"{self.name}"


class Transaction(models.Model):
    """
    Transaction model for storing the user transactions data with the following fields:
    - user: ForeignKey to the User model
    - category: ForeignKey to the Category model
    - type: CharField with choices of "income" and "expense"
    - amount: DecimalField for storing the transaction amount
    """
    TRANSACTION_TYPE_CHOICES = (
        ("income", "Income"),
        ("expense", "Expense"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    # django docs Managers
    objects = TransactionQuerySet.as_manager()

    def __str__(self) -> str:
        return f"{self.type} of {self.amount} on {self.date} by {self.user}"

    class Meta:
        ordering = ["-date"]
