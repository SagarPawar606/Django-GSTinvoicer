# Generated by Django 3.2.12 on 2022-06-20 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_delete_organizationname'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationldetials',
            name='org_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Organization Name'),
        ),
    ]