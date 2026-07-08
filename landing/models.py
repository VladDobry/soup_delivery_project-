from django.db import models


class SoupPrice(models.Model):
    class PriceGroup(models.TextChoices):
        DEFAULT = "default", "Базовые супы"
        UKHA = "ukha", "Уха"
        BROTH = "broth", "Коллагеновый бульон"

    class Volume(models.TextChoices):
        ONE_LITER = "1l", "1000гр"
        ONE_AND_HALF_LITER = "15l", "1600гр"
        TWO_LITERS = "2l", "2200гр"

    price_group = models.CharField("группа цен", max_length=20, choices=PriceGroup.choices)
    volume = models.CharField("объём", max_length=10, choices=Volume.choices)
    price_rub = models.PositiveIntegerField("цена, ₽")
    is_active = models.BooleanField("активна", default=True)
    sort_order = models.PositiveSmallIntegerField("порядок", default=0)

    class Meta:
        verbose_name = "цена супа"
        verbose_name_plural = "Цены супов"
        ordering = ("price_group", "sort_order", "volume")
        constraints = [
            models.UniqueConstraint(
                fields=("price_group", "volume"),
                name="unique_soup_price_group_volume",
            )
        ]

    def __str__(self):
        return f"{self.get_price_group_display()} · {self.get_volume_display()} · {self.price_rub} ₽"


class SetPrice(models.Model):
    title = models.CharField("позиция", max_length=80)
    price_rub = models.PositiveIntegerField("цена, ₽")
    caption = models.CharField("подпись", max_length=80, default="за порцию")
    is_active = models.BooleanField("активна", default=True)
    sort_order = models.PositiveSmallIntegerField("порядок", default=0)

    class Meta:
        verbose_name = "цена сета"
        verbose_name_plural = "Цены сетов"
        ordering = ("sort_order", "id")

    def __str__(self):
        return f"{self.title} · {self.price_rub} ₽"
