from django.contrib import admin

# Register your models here.
from .models import Favorite

class FavoriteAdmin(admin.ModelAdmin):
    class Meta:
        model = Favorite

admin.site.register(Favorite, FavoriteAdmin)
