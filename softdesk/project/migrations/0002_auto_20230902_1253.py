# Generated by Django 3.2.5 on 2023-09-02 10:53

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='issue',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 2, 12, 53, 39, 390267), editable=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 2, 12, 53, 39, 390267)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('dfba5ecc-26b9-4124-b224-6822da991d7c'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='contributor',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 2, 12, 53, 39, 390267), editable=False),
        ),
        migrations.AlterField(
            model_name='contributor',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 2, 12, 53, 39, 390267)),
        ),
        migrations.AlterField(
            model_name='contributor',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('dfba5ecc-26b9-4124-b224-6822da991d7c'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 2, 12, 53, 39, 390267), editable=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 2, 12, 53, 39, 390267)),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('8b1371ba-3f5f-4ecc-90c7-dbb15c9a2525'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 2, 12, 53, 39, 390267), editable=False),
        ),
        migrations.AlterField(
            model_name='issue',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 2, 12, 53, 39, 390267)),
        ),
        migrations.AlterField(
            model_name='issue',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('dfba5ecc-26b9-4124-b224-6822da991d7c'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('dfba5ecc-26b9-4124-b224-6822da991d7c'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
