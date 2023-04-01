# Generated by Django 3.2 on 2023-04-01 14:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_product_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='created',
            field=models.DateField(blank=True, default=datetime.datetime(2023, 4, 1, 19, 59, 29, 160117), null=True),
        ),
    ]
