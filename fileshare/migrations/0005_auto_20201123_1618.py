# Generated by Django 3.1.3 on 2020-11-23 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fileshare', '0004_fileevent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileshareperson',
            name='file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fileshare.file'),
        ),
    ]
