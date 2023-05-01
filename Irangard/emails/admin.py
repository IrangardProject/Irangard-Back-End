from django.contrib import admin

# Register your models here.
from emails.models import EmailQueue


class EmailAdmin(admin.ModelAdmin):
    list_display = ['email_title', 'email_body', 'sender', 'receiver', 'state']

    class Meta:
        model = EmailQueue


admin.site.register(EmailQueue, EmailAdmin)

