from django.db import migrations, models


def sync_delivery_type(apps, schema_editor):
    Order = apps.get_model("restaurant", "Order")
    for order in Order.objects.all():
        order.delivery_type = "pickup" if order.self_pickup else "delivery"
        order.kitchen_status = order.kitchen_status or "new"
        order.save(update_fields=["delivery_type", "kitchen_status"])


class Migration(migrations.Migration):

    dependencies = [
        ("restaurant", "0007_remove_dish_ingredients_delete_dishingredient_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="delivery_type",
            field=models.CharField(
                choices=[("delivery", "Delivery"), ("pickup", "Pickup")],
                default="delivery",
                max_length=16,
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="kitchen_status",
            field=models.CharField(
                choices=[("new", "New"), ("preparing", "Preparing"), ("completed", "Completed")],
                default="new",
                max_length=16,
            ),
        ),
        migrations.RunPython(sync_delivery_type, migrations.RunPython.noop),
    ]
