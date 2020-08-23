# Generated by Django 3.0.8 on 2020-08-12 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_auto_20200811_2225'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postspage',
            name='range',
        ),
        migrations.AddField(
            model_name='postspage',
            name='style',
            field=models.CharField(blank=True, choices=[('Antique', 'Antique'), ('Beads', 'Beads'), ('Bridal', 'Bridal'), ('Classic', 'Classic'), ('Ethnic/Vintage', 'Ethnic/Vintage'), ('Gold/Silver', 'Gold/Silver'), ('Stones', 'Stones'), ('Modern', 'Modern'), ('Metal', 'Metal'), ('Kundan', 'Kundan'), ('Handmade', 'Handmade'), ('Thread', 'Thread')], max_length=30, null=True),
        ),
    ]
