# Generated by Django 5.2.1 on 2025-05-19 18:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_customertask'),
    ]

    operations = [
        migrations.AddField(
            model_name='customertask',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='customers.customer'),
        ),
    ]
