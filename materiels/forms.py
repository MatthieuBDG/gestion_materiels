from django import forms
from .models import Materiel, Enseignant, Salle, Accessoire, ChangementPossesseur


class EmpruntForm(forms.ModelForm):
    ancien_possesseur = forms.ModelChoiceField(
        queryset=Enseignant.objects.all(),
        label='Ancien possesseur ',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    nouveau_possesseur = forms.ModelChoiceField(
        queryset=Enseignant.objects.all(),
        label='Nouveau possesseur ',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    date = forms.DateField(
        label='Date ',
        widget=forms.DateInput(attrs={'class': 'form-control'}),
    )
    lieu = forms.CharField(
        label='Lieu ',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    occasion = forms.CharField(
        label='Occasion ',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    objectif_utilisation = forms.CharField(
        label='Objectif d\'utilisation ',
        widget=forms.Textarea(attrs={'class': 'form-control'}),
    )
    materiel = forms.ModelChoiceField(
        queryset=Materiel.objects.all(),
        label='Matériel ',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    accessoires_presents = forms.ChoiceField(
        label='Accessoires Présents ',
        choices=[('True', 'Oui'), ('False', 'Non')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )
    etat_accessoires = forms.ChoiceField(
        label='État des accessoires ',
        choices=[('Très Mauvais', 'Très Mauvais'), ('Mauvais', 'Mauvais'), ('Correct', 'Correct'), ('Bon', 'Bon'),
                 ('Neuf', 'Neuf')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )

    class Meta:
        model = ChangementPossesseur
        fields = (
            'materiel', 'accessoires_presents', 'etat_accessoires', 'ancien_possesseur', 'nouveau_possesseur', 'date',
            'lieu', 'occasion', 'objectif_utilisation')


class SalleForm(forms.ModelForm):
    numero = forms.DecimalField(
        max_digits=3,
        decimal_places=3,
        label='Numero ',

        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Salle
        fields = ('numero',)


class EnseignantForm(forms.ModelForm):
    nom = forms.CharField(
        max_length=100,
        label='Nom & Prenom ',

        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Enseignant
        fields = ('nom',)

class AccessoireForm(forms.ModelForm):
    nom = forms.CharField(
        max_length=100,
        label='Nom',

        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Accessoire
        fields = ('nom',)

class MaterielForm(forms.ModelForm):
    nom = forms.CharField(
        max_length=100,
        label='Nom',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    budget_annuel = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label='Budget annuel',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    budget_projets = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label='Budget projets',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    budget_financements_exceptionnels = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label='Budget financements exceptionnels',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    acheteur = forms.ModelChoiceField(
        queryset=Enseignant.objects.all(),
        label='Acheteur',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    mandant = forms.ModelChoiceField(
        queryset=Enseignant.objects.all(),
        label='Mandant',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    proprietaire = forms.ModelChoiceField(
        queryset=Enseignant.objects.all(),
        label='Propriétaire',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    salle = forms.ModelChoiceField(
        queryset=Salle.objects.all(),
        label='Salle',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    possesseur = forms.ModelChoiceField(
        queryset=Enseignant.objects.all(),
        label='Possesseur',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    accessoires = forms.ModelMultipleChoiceField(
        queryset=Accessoire.objects.all(),
        label='Accessoires',
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        acheteur = cleaned_data.get('acheteur')
        mandant = cleaned_data.get('mandant')

        if not acheteur and not mandant:
            self.add_error(None, "Au moins l'acheteur ou le mandant doit être renseigné.")

    class Meta:
        model = Materiel
        fields = ('nom', 'budget_annuel', 'budget_projets', 'budget_financements_exceptionnels',
                  'acheteur', 'mandant', 'proprietaire', 'salle', 'possesseur', 'accessoires')
