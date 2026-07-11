from django.db import migrations


PRICE_BY_VOLUME = {
    "1l": 1550,
    "15l": 2250,
    "2l": 2850,
}


OLD_PRICE_BY_GROUP_VOLUME = {
    ("default", "1l"): 2500,
    ("default", "15l"): 3750,
    ("default", "2l"): 4500,
    ("ukha", "1l"): 3000,
    ("ukha", "15l"): 4250,
    ("ukha", "2l"): 5000,
    ("broth", "2l"): 2500,
}


def update_soup_prices(apps, schema_editor):
    SoupPrice = apps.get_model("landing", "SoupPrice")

    for volume, price_rub in PRICE_BY_VOLUME.items():
        SoupPrice.objects.filter(volume=volume).update(price_rub=price_rub)


def restore_soup_prices(apps, schema_editor):
    SoupPrice = apps.get_model("landing", "SoupPrice")

    for (price_group, volume), price_rub in OLD_PRICE_BY_GROUP_VOLUME.items():
        SoupPrice.objects.filter(price_group=price_group, volume=volume).update(
            price_rub=price_rub,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("landing", "0004_update_default_volume_labels"),
    ]

    operations = [
        migrations.RunPython(update_soup_prices, restore_soup_prices),
    ]
