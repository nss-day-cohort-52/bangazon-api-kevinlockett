# Generated by Django 3.2.12 on 2022-03-03 03:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bangazon_api', '0005_auto_20220302_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='completed_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bangazon_api.paymenttype'),
        ),
    ]
