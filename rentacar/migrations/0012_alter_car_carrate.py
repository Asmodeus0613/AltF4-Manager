# Generated by Django 4.2.6 on 2023-10-25 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentacar', '0011_alter_order_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='carRate',
            field=models.FloatField(),
        ),
    ]
