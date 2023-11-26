from django.contrib import admin
from .models import User


class AccountAmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'id')
    search_fields = ('first_name', 'last_name', 'email')
    readonly_fields = ('date_create', )

admin.site.register(User, AccountAmin)
