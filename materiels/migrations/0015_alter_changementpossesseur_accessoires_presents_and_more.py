# Generated by Django 4.2.3 on 2023-07-06 13:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("materiels", "0014_alter_accessoire_etat"),
    ]

    operations = [
        migrations.AlterField(
            model_name="changementpossesseur",
            name="accessoires_presents",
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name="changementpossesseur",
            name="etat",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
