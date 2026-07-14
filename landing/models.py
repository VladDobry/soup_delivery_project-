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


class SoupMathRow(models.Model):
    price_rub = models.PositiveIntegerField("цена, ₽")
    total_weight_label = models.CharField("общий вес", max_length=40)
    is_active = models.BooleanField("активна", default=True)
    sort_order = models.PositiveSmallIntegerField("порядок", default=0)

    class Meta:
        verbose_name = "строка супер математики"
        verbose_name_plural = "СУПер математика"
        ordering = ("sort_order", "id")

    def __str__(self):
        return f"{self.price_rub} ₽ · {self.total_weight_label}"


class SoupMathTerm(models.Model):
    class VisualType(models.TextChoices):
        JAR_1L = "jar_1l", "Банка 1 л"
        JAR_15L = "jar_15l", "Банка 1,5 л"
        JAR_BORSCH_1L = "jar_borsch_1l", "Банка борща 1 л"
        TAKEAWAY_035L = "takeaway_035l", "Тарелка с собой 0,35 л"

    row = models.ForeignKey(
        SoupMathRow,
        on_delete=models.CASCADE,
        related_name="terms",
        verbose_name="строка",
    )
    volume_label = models.CharField("объём", max_length=40)
    visual_type = models.CharField("картинка", max_length=30, choices=VisualType.choices)
    sort_order = models.PositiveSmallIntegerField("порядок", default=0)

    class Meta:
        verbose_name = "слагаемое супер математики"
        verbose_name_plural = "Слагаемые супер математики"
        ordering = ("sort_order", "id")

    def __str__(self):
        return f"{self.volume_label} · {self.get_visual_type_display()}"


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
