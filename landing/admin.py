from django.contrib import admin

from .models import SetPrice, SoupPrice


@admin.register(SoupPrice)
class SoupPriceAdmin(admin.ModelAdmin):
    list_display = (
        "price_group",
        "volume",
        "price_rub",
        "is_active",
        "sort_order",
    )
    list_editable = ("price_rub", "is_active", "sort_order")
    list_filter = ("price_group", "volume", "is_active")
    search_fields = ("price_group", "volume")
    ordering = ("price_group", "sort_order", "volume")


@admin.register(SetPrice)
class SetPriceAdmin(admin.ModelAdmin):
    list_display = ("title", "price_rub", "caption", "is_active", "sort_order")
    list_editable = ("price_rub", "caption", "is_active", "sort_order")
    list_filter = ("is_active",)
    search_fields = ("title", "caption")
    ordering = ("sort_order", "id")
