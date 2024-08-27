from datetime import datetime
import factory
from tracker.models import Category, Transaction, User


class UserFactory(factory.django.DjangoModelFactory):
    """
    This class is a factory for the User model.
    It creates a new user with a unique username and random first and last names.
    """
    class Meta:
        model = User
        django_get_or_create = ("username",)

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Sequence(lambda n: "user%d" % n)


class CategoryFactory(factory.django.DjangoModelFactory):
    """
    This class is a factory for the Category model.
    It creates a new category with a unique name from the list of names provided in the factory.Iterator.
    """
    class Meta:
        model = Category
        django_get_or_create = ("name",)

    name = factory.Iterator(["Bills", "Housing", "Salary", "Food", "Social"])


class TransactionFactory(factory.django.DjangoModelFactory):
    """
    This class is a factory for the Transaction model.
    It creates a new transaction with a random user, category, amount, date, and type.
    """
    class Meta:
        model = Transaction

    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    amount = 5
    date = factory.Faker(
        "date_between",
        start_date=datetime(year=2022, month=1, day=1).date(),
        end_date=datetime.now().date(),
    )
    type = factory.Iterator([x[0]
                            for x in Transaction.TRANSACTION_TYPE_CHOICES])
