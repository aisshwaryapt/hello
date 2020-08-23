# Generated by Django 3.0.8 on 2020-08-11 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_auto_20200811_1938'),
    ]

    operations = [
        migrations.AddField(
            model_name='postspage',
            name='ran',
            field=models.CharField(blank=True, choices=[('Below 100', 'B'), ('100-200', '2'), ('200-300', '3'), ('300-400', '4'), ('400-500', '5'), ('500-600', '6'), ('600-700', '7'), ('700-800', '8'), ('800-900', '9'), ('Above 1000', 'A')], max_length=30, null=True),
        ),
    ]
