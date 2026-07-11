from django.db import models


class SoupPrice(models.Model):
    class PriceGroup(models.TextChoices):
        DEFAULT = "default", "Базовые супы"
        UKHA = "ukha", "Уха"
        BROTH = "broth", "Коллагеновый бульон"

    class Volume(models.TextChoices):
        ONE_LITER = "1l", "1000гр"
        ONE_AND_HALF_LITER = "15l", "1500гр"
        TWO_LITERS = "2l", "2000гр"

    price_group = models.CharField("группа цен", max_length=20, choices=PriceGroup.choices)
    volume = models.CharField("объём", max_length=10, choices=Volume.choices)
    volume_label = models.CharField("граммовка", max_length=40, default="")
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
        return f"{self.get_price_group_display()} · {self.display_volume_label} · {self.price_rub} ₽"

    @property
    def display_volume_label(self):
        return self.volume_label or self.get_volume_display()


class SetPrice(models.Model):
    title = models.CharField("позиция", max_length=80)
    price_rub = models.PositiveIntegerField("цена, ₽")
    caption = models.CharField("граммовка под ценой", max_length=80, default="350мл")
    is_active = models.BooleanField("активна", default=True)
    sort_order = models.PositiveSmallIntegerField("порядок", default=0)

    class Meta:
        verbose_name = "цена сета"
        verbose_name_plural = "Цены сетов"
        ordering = ("sort_order", "id")

    def __str__(self):
        return f"{self.title} · {self.price_rub} ₽"


class SiteGrammageSetting(models.Model):
    class SettingKey(models.TextChoices):
        GIFT_PORTION = "gift_portion", "Граммовка подарочного супа"

    key = models.CharField("настройка", max_length=40, choices=SettingKey.choices, unique=True)
    value = models.CharField("граммовка", max_length=40)

    class Meta:
        verbose_name = "граммовка сайта"
        verbose_name_plural = "Граммовки сайта"
        ordering = ("key",)

    def __str__(self):
        return f"{self.get_key_display()} · {self.value}"
