from django.db import migrations, models


SOUP_PRICE_SEED = [
    ("default", "1l", 2500, 10),
    ("default", "15l", 3750, 20),
    ("default", "2l", 4500, 30),
    ("ukha", "1l", 3000, 10),
    ("ukha", "15l", 4250, 20),
    ("ukha", "2l", 5000, 30),
    ("broth", "2l", 2500, 30),
]

SET_PRICE_SEED = [
    ("350мл", 750, "за порцию", 10),
    ("Уха", 850, "за порцию", 20),
]


def seed_prices(apps, schema_editor):
    SoupPrice = apps.get_model("landing", "SoupPrice")
    SetPrice = apps.get_model("landing", "SetPrice")

    for price_group, volume, price_rub, sort_order in SOUP_PRICE_SEED:
        SoupPrice.objects.update_or_create(
            price_group=price_group,
            volume=volume,
            defaults={
                "price_rub": price_rub,
                "sort_order": sort_order,
                "is_active": True,
            },
        )

    for title, price_rub, caption, sort_order in SET_PRICE_SEED:
        SetPrice.objects.update_or_create(
            title=title,
            defaults={
                "price_rub": price_rub,
                "caption": caption,
                "sort_order": sort_order,
                "is_active": True,
            },
        )


def unseed_prices(apps, schema_editor):
    SoupPrice = apps.get_model("landing", "SoupPrice")
    SetPrice = apps.get_model("landing", "SetPrice")

    SoupPrice.objects.filter(
        price_group__in={price_group for price_group, *_ in SOUP_PRICE_SEED}
    ).delete()
    SetPrice.objects.filter(title__in={title for title, *_ in SET_PRICE_SEED}).delete()


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SetPrice",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=80, verbose_name="позиция")),
                ("price_rub", models.PositiveIntegerField(verbose_name="цена, ₽")),
                ("caption", models.CharField(default="за порцию", max_length=80, verbose_name="подпись")),
                ("is_active", models.BooleanField(default=True, verbose_name="активна")),
                ("sort_order", models.PositiveSmallIntegerField(default=0, verbose_name="порядок")),
            ],
            options={
                "verbose_name": "цена сета",
                "verbose_name_plural": "Цены сетов",
                "ordering": ("sort_order", "id"),
            },
        ),
        migrations.CreateModel(
            name="SoupPrice",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "price_group",
                    models.CharField(
                        choices=[
                            ("default", "Базовые супы"),
                            ("ukha", "Уха"),
                            ("broth", "Коллагеновый бульон"),
                        ],
                        max_length=20,
                        verbose_name="группа цен",
                    ),
                ),
                (
                    "volume",
                    models.CharField(
                        choices=[("1l", "1000гр"), ("15l", "1600гр"), ("2l", "2200гр")],
                        max_length=10,
                        verbose_name="объём",
                    ),
                ),
                ("price_rub", models.PositiveIntegerField(verbose_name="цена, ₽")),
                ("is_active", models.BooleanField(default=True, verbose_name="активна")),
                ("sort_order", models.PositiveSmallIntegerField(default=0, verbose_name="порядок")),
            ],
            options={
                "verbose_name": "цена супа",
                "verbose_name_plural": "Цены супов",
                "ordering": ("price_group", "sort_order", "volume"),
            },
        ),
        migrations.AddConstraint(
            model_name="soupprice",
            constraint=models.UniqueConstraint(
                fields=("price_group", "volume"),
                name="unique_soup_price_group_volume",
            ),
        ),
        migrations.RunPython(seed_prices, unseed_prices),
    ]
