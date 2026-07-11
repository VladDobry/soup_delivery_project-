from django.db import migrations


def update_default_volume_labels(apps, schema_editor):
    SoupPrice = apps.get_model("landing", "SoupPrice")

    SoupPrice.objects.filter(volume="15l", volume_label="1600гр").update(
        volume_label="1500гр",
    )
    SoupPrice.objects.filter(volume="2l", volume_label="2200гр").update(
        volume_label="2000гр",
    )


def restore_default_volume_labels(apps, schema_editor):
    SoupPrice = apps.get_model("landing", "SoupPrice")

    SoupPrice.objects.filter(volume="15l", volume_label="1500гр").update(
        volume_label="1600гр",
    )
    SoupPrice.objects.filter(volume="2l", volume_label="2000гр").update(
        volume_label="2200гр",
    )


class Migration(migrations.Migration):
    dependencies = [
        ("landing", "0003_add_editable_grammages"),
    ]

    operations = [
        migrations.RunPython(update_default_volume_labels, restore_default_volume_labels),
    ]
