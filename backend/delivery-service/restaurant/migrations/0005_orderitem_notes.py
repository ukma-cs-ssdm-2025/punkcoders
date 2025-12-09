from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("restaurant", "0004_order_orderitem"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderitem",
            name="notes",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
    ]
