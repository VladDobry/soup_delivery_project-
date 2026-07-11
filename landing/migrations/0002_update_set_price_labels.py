from django.db import migrations


def update_set_price_labels(apps, schema_editor):
    SetPrice = apps.get_model("landing", "SetPrice")

    SetPrice.objects.filter(title="350мл", caption="за порцию").update(
        title="любой суп*",
        caption="350мл",
    )
    SetPrice.objects.filter(title="Уха", caption="за порцию").update(
        title="*Уха",
        caption="350мл",
    )


def restore_set_price_labels(apps, schema_editor):
    SetPrice = apps.get_model("landing", "SetPrice")

    SetPrice.objects.filter(title="любой суп*", caption="350мл").update(
        title="350мл",
        caption="за порцию",
    )
    SetPrice.objects.filter(title="*Уха", caption="350мл").update(
        title="Уха",
        caption="за порцию",
    )


class Migration(migrations.Migration):
    dependencies = [
        ("landing", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(update_set_price_labels, restore_set_price_labels),
    ]
