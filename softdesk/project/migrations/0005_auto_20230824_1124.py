# Generated by Django 3.2.5 on 2023-08-24 09:24

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_auto_20230823_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 24, 11, 24, 50, 487959), editable=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 24, 11, 24, 50, 487959)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('dfbdd839-6d19-4655-86df-4c79ad80a16e'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='contributor',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 24, 11, 24, 50, 487959), editable=False),
        ),
        migrations.AlterField(
            model_name='contributor',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 24, 11, 24, 50, 487959)),
        ),
        migrations.AlterField(
            model_name='contributor',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('dfbdd839-6d19-4655-86df-4c79ad80a16e'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 24, 11, 24, 50, 487959), editable=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 24, 11, 24, 50, 487959)),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('dfbdd839-6d19-4655-86df-4c79ad80a16e'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 24, 11, 24, 50, 487959), editable=False),
        ),
        migrations.AlterField(
            model_name='issue',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 24, 11, 24, 50, 487959)),
        ),
        migrations.AlterField(
            model_name='issue',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('dfbdd839-6d19-4655-86df-4c79ad80a16e'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('dfbdd839-6d19-4655-86df-4c79ad80a16e'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
