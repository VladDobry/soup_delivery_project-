from django.db import migrations, models
import django.db.models.deletion


SOUP_MATH_SEED = [
    {
        "sort_order": 10,
        "price_rub": 2850,
        "total_weight_label": "ЗА 2000 Г",
        "terms": [
            ("jar_1l", "1 л", 10),
            ("jar_1l", "1 л", 20),
        ],
    },
    {
        "sort_order": 20,
        "price_rub": 3550,
        "total_weight_label": "ЗА 2500 Г",
        "terms": [
            ("jar_1l", "1 л", 10),
            ("jar_15l", "1,5 л", 20),
        ],
    },
    {
        "sort_order": 30,
        "price_rub": 2550,
        "total_weight_label": "ЗА 1700 Г",
        "terms": [
            ("takeaway_035l", "0,35 л", 10),
            ("takeaway_035l", "0,35 л", 20),
            ("jar_borsch_1l", "1 л", 30),
        ],
    },
]


def seed_soup_math(apps, schema_editor):
    SoupMathRow = apps.get_model("landing", "SoupMathRow")
    SoupMathTerm = apps.get_model("landing", "SoupMathTerm")

    for row_data in SOUP_MATH_SEED:
        row, _created = SoupMathRow.objects.update_or_create(
            sort_order=row_data["sort_order"],
            defaults={
                "price_rub": row_data["price_rub"],
                "total_weight_label": row_data["total_weight_label"],
                "is_active": True,
            },
        )
        row.terms.all().delete()
        for visual_type, volume_label, sort_order in row_data["terms"]:
            SoupMathTerm.objects.create(
                row=row,
                visual_type=visual_type,
                volume_label=volume_label,
                sort_order=sort_order,
            )


def unseed_soup_math(apps, schema_editor):
    SoupMathRow = apps.get_model("landing", "SoupMathRow")
    SoupMathRow.objects.filter(
        sort_order__in=[row_data["sort_order"] for row_data in SOUP_MATH_SEED],
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("landing", "0005_update_soup_prices"),
    ]

    operations = [
        migrations.CreateModel(
            name="SoupMathRow",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("price_rub", models.PositiveIntegerField(verbose_name="цена, ₽")),
                (
                    "total_weight_label",
                    models.CharField(max_length=40, verbose_name="общий вес"),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="активна")),
                ("sort_order", models.PositiveSmallIntegerField(default=0, verbose_name="порядок")),
            ],
            options={
                "verbose_name": "строка супер математики",
                "verbose_name_plural": "СУПер математика",
                "ordering": ("sort_order", "id"),
            },
        ),
        migrations.CreateModel(
            name="SoupMathTerm",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("volume_label", models.CharField(max_length=40, verbose_name="объём")),
                (
                    "visual_type",
                    models.CharField(
                        choices=[
                            ("jar_1l", "Банка 1 л"),
                            ("jar_15l", "Банка 1,5 л"),
                            ("jar_borsch_1l", "Банка борща 1 л"),
                            ("takeaway_035l", "Тарелка с собой 0,35 л"),
                        ],
                        max_length=30,
                        verbose_name="картинка",
                    ),
                ),
                ("sort_order", models.PositiveSmallIntegerField(default=0, verbose_name="порядок")),
                (
                    "row",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="terms",
                        to="landing.soupmathrow",
                        verbose_name="строка",
                    ),
                ),
            ],
            options={
                "verbose_name": "слагаемое супер математики",
                "verbose_name_plural": "Слагаемые супер математики",
                "ordering": ("sort_order", "id"),
            },
        ),
        migrations.RunPython(seed_soup_math, unseed_soup_math),
    ]
