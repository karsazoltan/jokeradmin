# Generated by Django 3.2.5 on 2021-08-26 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210826_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetail',
            name='systemuser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.systemuser'),
        ),
    ]
