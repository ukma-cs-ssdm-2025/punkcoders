from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("restaurant", "0004_order_orderitem"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="kitchen_status",
            field=models.CharField(
                choices=[("new", "New"), ("preparing", "Preparing"), ("completed", "Completed")],
                db_index=True,
                default="new",
                max_length=16,
            ),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="notes",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
    ]
