from django.contrib import admin

from .models import Letting
from .models import Profile


admin.site.register(Letting)
admin.site.register(Profile)
