from django.db import models


class Enseignant(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Salle(models.Model):
    numero = models.CharField(max_length=10)

    def __str__(self):
        return self.numero


class Materiel(models.Model):
    nom = models.CharField(max_length=100)
    budget_annuel = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    budget_projets = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    budget_financements_exceptionnels = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    acheteur = models.ForeignKey(Enseignant, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='materiels_achetes')
    mandant = models.ForeignKey(Enseignant, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='materiels_mandates')
    proprietaire = models.ForeignKey(Enseignant, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='materiels_propriete')
    salle = models.ForeignKey(Salle, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='materiels_salle_num')
    possesseur = models.ForeignKey(Enseignant, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='materiels_possedes')
    accompagnements = models.ManyToManyField('self', symmetrical=False, blank=True)

    def __str__(self):
        return self.nom


class ChangementPossesseur(models.Model):
    materiel = models.ForeignKey(Materiel, on_delete=models.CASCADE)
    ancien_possesseur = models.ForeignKey(Enseignant, on_delete=models.CASCADE, related_name='chgmt_possesseur_ancien')
    nouveau_possesseur = models.ForeignKey(Enseignant, on_delete=models.CASCADE,
                                           related_name='chgmt_possesseur_nouveau')
    date = models.DateField()
    lieu = models.CharField(max_length=100)
    occasion = models.CharField(max_length=100)
    objectif_utilisation = models.TextField()
    accessoires_presents = models.BooleanField(default=False, null=True)
    etat = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"ChangementPossesseur {self.id}"


class Accessoire(models.Model):
    nom = models.CharField(max_length=100)
    etat = models.CharField(max_length=100, null=True, blank=True)
    materiels = models.ManyToManyField(Materiel, related_name='accessoires')

    def __str__(self):
        return self.nom

class Etat(models.Model):
    libelle = models.CharField(max_length=20)

    def __str__(self):
        return self.libelle
