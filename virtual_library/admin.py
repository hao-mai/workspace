from django.contrib import admin
from .models import Genre,Book,Checkout
# Register your models here.

admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(Checkout)
