from django.contrib import admin

from finances.models import Account, Category, Ticket, Transaction

admin.site.register(Account)
admin.site.register(Category)
admin.site.register(Ticket)
admin.site.register(Transaction)
