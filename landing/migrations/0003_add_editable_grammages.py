from django.db import migrations, models


VOLUME_LABELS = {
    "1l": "1000гр",
    "15l": "1500гр",
    "2l": "2000гр",
}


def seed_grammages(apps, schema_editor):
    SoupPrice = apps.get_model("landing", "SoupPrice")
    SiteGrammageSetting = apps.get_model("landing", "SiteGrammageSetting")

    for volume, label in VOLUME_LABELS.items():
        SoupPrice.objects.filter(volume=volume, volume_label="").update(volume_label=label)

    SiteGrammageSetting.objects.update_or_create(
        key="gift_portion",
        defaults={"value": "250 гр"},
    )


def unseed_grammages(apps, schema_editor):
    SiteGrammageSetting = apps.get_model("landing", "SiteGrammageSetting")
    SiteGrammageSetting.objects.filter(key="gift_portion").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("landing", "0002_update_set_price_labels"),
    ]

    operations = [
        migrations.AddField(
            model_name="soupprice",
            name="volume_label",
            field=models.CharField(default="", max_length=40, verbose_name="граммовка"),
        ),
        migrations.AlterField(
            model_name="setprice",
            name="caption",
            field=models.CharField(default="350мл", max_length=80, verbose_name="граммовка под ценой"),
        ),
        migrations.CreateModel(
            name="SiteGrammageSetting",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "key",
                    models.CharField(
                        choices=[("gift_portion", "Граммовка подарочного супа")],
                        max_length=40,
                        unique=True,
                        verbose_name="настройка",
                    ),
                ),
                ("value", models.CharField(max_length=40, verbose_name="граммовка")),
            ],
            options={
                "verbose_name": "граммовка сайта",
                "verbose_name_plural": "Граммовки сайта",
                "ordering": ("key",),
            },
        ),
        migrations.RunPython(seed_grammages, unseed_grammages),
    ]
