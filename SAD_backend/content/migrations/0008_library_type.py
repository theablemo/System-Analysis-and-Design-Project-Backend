# Generated by Django 3.2.3 on 2022-08-12 16:20

import content.models.content
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0007_fileaccess'),
    ]

    operations = [
        migrations.AddField(
            model_name='library',
            name='type',
            field=models.CharField(default=content.models.content.ContentType.get_default_type_pk, max_length=30),
        ),
    ]
