# Generated by Django 2.1.1 on 2021-09-02 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jokerauth', '0006_alter_sshkey_pubkey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sshkey',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
