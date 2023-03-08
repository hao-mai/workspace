from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F, Value, Case, When

class Genre(models.Model):
    """
    Genre of the book
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Library that will store and manage books
    """
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.ManyToManyField(Genre, related_name='genres')
    num_pages = models.IntegerField()
    available = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["title"]
        verbose_name = "Book"
        verbose_name_plural = "Books"
        default_permissions = ("add", "change", "delete", "view")

    def __str__(self):
        return str(self.title)

class Checkout(models.Model):
    book = models.ForeignKey('Book',on_delete=models.RESTRICT,null=True)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    checkout_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['book']

    def __str__(self):
        return f"{self.borrower.email} checked out {self.book.title}"

@receiver(post_save, sender=Checkout)
def update_book_availability(sender, instance, created, **kwargs):
    if created:
        book = instance.book
        # we're using Case and When expressions to conditionally
        # set the available field based on the quantity field.
        # If quantity is greater than 1, we set available to True,
        # otherwise we set it to False.
        Book.objects.filter(pk=book.pk).update(
            quantity=F('quantity') - 1,
            available=Case(
            When(quantity__gt=1, then=Value(True)),
            default=Value(False)
        )
    )
    elif instance.return_date is not None:
        book = instance.book
        Book.objects.filter(pk=book.pk).update(
            quantity=F('quantity') + 1,
            available=True
        )
