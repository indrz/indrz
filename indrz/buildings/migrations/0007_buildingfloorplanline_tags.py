# Generated by Django 2.2.6 on 2019-11-29 21:02

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0006_buildingfloorspace_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildingfloorplanline',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=150), blank=True, null=True, size=None), blank=True, null=True, size=None),
        ),
    ]
