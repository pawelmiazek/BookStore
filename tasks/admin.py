from django.contrib import admin

from tasks.models import Account, Book, Operation, Purchase

admin.site.register(Account)
admin.site.register(Operation)
admin.site.register(Book)
admin.site.register(Purchase)
