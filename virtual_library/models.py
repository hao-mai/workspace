from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    genres = models.ManyToManyField(Genre)
    num_pages = models.IntegerField()
    available = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["title"]
        verbose_name = "Book"
        verbose_name_plural = "Books"
        default_permissions = ("add", "change", "delete", "view")

    def save(self, *args, **kwargs):
        if self.quantity > 0:
            self.is_available = True
        else:
            self.is_available = False
        super().save(*args, **kwargs)

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
        book.quantity -= 1
        book.save()

        if book.quantity == 0:
            book.is_available = False
            book.save()
    elif not created and instance.return_date is not None:
        book = instance.book
        book.quantity += 1
        book.save()

        if book.is_available == False:
            book.is_available = True
            book.save()
