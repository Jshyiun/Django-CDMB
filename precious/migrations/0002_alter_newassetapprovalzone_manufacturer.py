# Generated by Django 4.0.1 on 2022-02-12 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('precious', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newassetapprovalzone',
            name='manufacturer',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='生产厂商'),
        ),
    ]
