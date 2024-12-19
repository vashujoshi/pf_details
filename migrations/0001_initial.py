# Generated by Django 5.1.4 on 2024-12-17 17:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, unique=True)),
                ("registration_number", models.CharField(max_length=50, unique=True)),
                ("address", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="Employee",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("pf_number", models.CharField(max_length=50, unique=True)),
                ("date_of_joining", models.DateField()),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="employees",
                        to="pf_tracker.company",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PFPayment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("month", models.DateField()),
                (
                    "employee_contribution",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "employer_contribution",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "total_contribution",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payments",
                        to="pf_tracker.employee",
                    ),
                ),
            ],
            options={
                "unique_together": {("employee", "month")},
            },
        ),
    ]