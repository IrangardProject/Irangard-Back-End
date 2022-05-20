from django.contrib import admin
from .models import *


admin.site.register(User)
admin.site.register(Verification)
admin.site.register(Token)
admin.site.register(SpecialUser)
admin.site.register(StagedPayments)
admin.site.register(Tour)
admin.site.register(DiscountCode)
admin.site.register(Transaction)