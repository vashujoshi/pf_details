# Generated by Django 5.1.4 on 2024-12-19 03:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pf_tracker", "0004_company_hello"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="company",
            name="hello",
        ),
    ]
