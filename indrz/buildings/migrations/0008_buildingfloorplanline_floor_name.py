# Generated by Django 2.2.5 on 2019-09-21 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0007_auto_20190921_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildingfloorplanline',
            name='floor_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='floor name'),
        ),
    ]
