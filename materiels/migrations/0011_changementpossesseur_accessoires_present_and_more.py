# Generated by Django 4.2.3 on 2023-07-06 11:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("materiels", "0010_remove_enseignant_prenom"),
    ]

    operations = [
        migrations.AddField(
            model_name="changementpossesseur",
            name="accessoires_present",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="changementpossesseur",
            name="etat_accessoires",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
