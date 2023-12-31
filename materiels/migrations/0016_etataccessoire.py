# Generated by Django 4.2.3 on 2023-07-06 14:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("materiels", "0015_alter_changementpossesseur_accessoires_presents_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="EtatAccessoire",
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
                (
                    "etat",
                    models.CharField(
                        choices=[
                            ("Très Mauvais", "Très Mauvais"),
                            ("Mauvais", "Mauvais"),
                            ("Correct", "Correct"),
                            ("Bon", "Bon"),
                            ("Neuf", "Neuf"),
                        ],
                        max_length=50,
                    ),
                ),
            ],
        ),
    ]
