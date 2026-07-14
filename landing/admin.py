from django.contrib import admin

from .models import SetPrice, SoupMathRow, SoupMathTerm, SoupPrice


@admin.register(SoupPrice)
class SoupPriceAdmin(admin.ModelAdmin):
    list_display = (
        "price_group",
        "volume",
        "volume_label",
        "price_rub",
        "is_active",
        "sort_order",
    )
    list_editable = ("volume_label", "price_rub", "is_active", "sort_order")
    list_filter = ("price_group", "volume", "is_active")
    search_fields = ("price_group", "volume", "volume_label")
    ordering = ("price_group", "sort_order", "volume")


@admin.register(SetPrice)
class SetPriceAdmin(admin.ModelAdmin):
    list_display = ("title", "price_rub", "caption", "is_active", "sort_order")
    list_editable = ("price_rub", "caption", "is_active", "sort_order")
    list_filter = ("is_active",)
    search_fields = ("title", "caption")
    ordering = ("sort_order", "id")


class SoupMathTermInline(admin.TabularInline):
    model = SoupMathTerm
    extra = 0
    fields = ("sort_order", "visual_type", "volume_label")
    ordering = ("sort_order", "id")


@admin.register(SoupMathRow)
class SoupMathRowAdmin(admin.ModelAdmin):
    list_display = ("sort_order", "is_active", "price_rub", "total_weight_label")
    list_editable = ("is_active", "price_rub", "total_weight_label")
    list_filter = ("is_active",)
    ordering = ("sort_order", "id")
    inlines = (SoupMathTermInline,)
