# Generated by Django 5.1.6 on 2025-02-13 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foodName', models.CharField(max_length=255)),
                ('foodCategory', models.CharField(max_length=255)),
            ],
        ),
    ]
