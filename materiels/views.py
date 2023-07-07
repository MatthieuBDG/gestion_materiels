from django.shortcuts import render, redirect, get_object_or_404
from .forms import EnseignantForm, MaterielForm, SalleForm, EmpruntForm,AccessoireForm
from .models import Enseignant, Materiel, Salle, ChangementPossesseur, Accessoire
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
import logging

logger = logging.getLogger('django')


def home(request):
    return render(request, 'home.html')


def get_accessoires(materiel_id):
    materiel = get_object_or_404(Materiel, id=materiel_id)
    accessoires = Accessoire.objects.filter(materiels=materiel)
    return list(accessoires)


def emprunts(request):
    query = request.GET.get('q')  # Récupère le paramètre de recherche 'q' depuis l'URL
    emprunts = ChangementPossesseur.objects.all()

    if query:
        emprunts = emprunts.filter(
            Q(lieu__icontains=query) |  # Recherche par le lieu
            Q(materiel__nom__icontains=query) |  # Recherche par le nom du matériel
            Q(ancien_possesseur__nom__icontains=query) |  # Recherche par le nom de l'ancien possesseur
            Q(nouveau_possesseur__nom__icontains=query) |  # Recherche par le nom du nouveau possesseur
            Q(date__icontains=query) |  # Recherche par la date
            Q(occasion__icontains=query) |  # Recherche par l'occasion
            Q(objectif_utilisation__icontains=query) |  # Recherche par l'objectif d'utilisation
            Q(etat__icontains=query)  # Recherche par état des accessoires
        )

    context = {
        'emprunts': emprunts,
        'query': query  # Ajoute la requête de recherche dans le contexte pour l'afficher dans le template
    }
    return render(request, 'emprunts/list.html', context)


def materiels(request):
    query = request.GET.get('q')  # Récupère le paramètre de recherche 'q' depuis l'URL
    materiels = Materiel.objects.all()

    if query:
        materiels = materiels.filter(
            Q(nom__icontains=query) |  # Recherche par nom
            Q(acheteur__nom__icontains=query) |  # Recherche par nom de l'acheteur
            Q(mandant__nom__icontains=query) |  # Recherche par nom du mandant
            Q(possesseur__nom__icontains=query) |  # Recherche par nom du possesseur
            Q(proprietaire__nom__icontains=query) |  # Recherche par nom du proprietaire
            Q(salle__numero__icontains=query)  # Recherche par numéro de salle
        )
    context = {
        'materiels': materiels,
        'query': query  # Ajoute la requête de recherche dans le contexte pour l'afficher dans le template
    }
    return render(request, 'materiels/list.html', context)


def accessoires(request):
    query = request.GET.get('q')  # Récupère le paramètre de recherche 'q' depuis l'URL
    accessoires = Accessoire.objects.all()

    if query:
        accessoires = accessoires.filter(
            Q(nom__icontains=query) |  # Recherche par nom
            Q(etat__icontains=query)  # Recherche par etat
        )
    context = {
        'accessoires': accessoires,
        'query': query  # Ajoute la requête de recherche dans le contexte pour l'afficher dans le template
    }
    return render(request, 'accessoires/list.html', context)

def enseignants(request):
    query = request.GET.get('q')  # Récupère le paramètre de recherche 'q' depuis l'URL
    enseignants = Enseignant.objects.all()

    if query:
        enseignants = enseignants.filter(
            nom__icontains=query)  # Filtre les enseignants dont le nom contient la requête de recherche

    context = {
        'enseignants': enseignants,
        'query': query  # Ajoute la requête de recherche dans le contexte pour l'afficher dans le template
    }
    return render(request, 'enseignants/list.html', context)


def salles(request):
    query = request.GET.get('q')  # Récupère le paramètre de recherche 'q' depuis l'URL
    salles = Salle.objects.all()

    if query:
        salles = salles.filter(
            numero__icontains=query)  # Filtre les salles dont le numéro contient la requête de recherche

    context = {
        'salles': salles,
        'query': query  # Ajoute la requête de recherche dans le contexte pour l'afficher dans le template
    }
    return render(request, 'salles/list.html', context)


def ajouter_salle(request):
    if request.method == 'POST':
        form = SalleForm(request.POST)
        if form.is_valid():
            salle = form.save(commit=False)  # Enregistre la salle dans une instance non sauvegardée
            numero = salle.numero

            # Vérification si la salle existe déjà dans la base de données
            if Salle.objects.filter(numero=numero).exists():
                form.add_error('numero', 'Cette salle existe déjà.')
            else:
                salle.save()  # Sauvegarde la salle dans la base de données
                messages.success(request, "Salle ajouté avec succès.")  # Message de confirmation
                # Rediriger vers une autre page après avoir ajouté l'enseignant
                return redirect('salles')
        else:
            messages.error(request, "Erreur lors de la saisie du formulaire.")
    else:
        form = SalleForm()

    context = {
        'form': form,
    }
    return render(request, 'salles/add.html', context)


def ajouter_emprunt(request):
    if request.method == 'POST':
        form = EmpruntForm(request.POST)
        if form.is_valid():
            emprunt = form.save(commit=False)
            emprunt.etat = form.cleaned_data['etat_accessoires']
            emprunt.save()

            materiel = emprunt.materiel  # Obtenir l'instance de Materiel

            # Mettre à jour les propriétés de l'instance
            materiel.possesseur = emprunt.nouveau_possesseur
            materiel.save()  # Appeler la méthode save() sur l'instance de Materiel

            if emprunt.accessoires_presents:
                # Récupérer le matériel lié à l'emprunt
                accessoires = get_accessoires(materiel.id)

                for accessoire in accessoires:
                    logger.info(accessoire.id)
                    accessoire.etat = form.cleaned_data['etat_accessoires']
                    accessoire.save()
            messages.success(request, "Emprunt ajouté avec succès.")  # Message de confirmation
            return redirect('emprunts')
        else:
            messages.error(request, "Erreur lors de la saisie du formulaire.")
    else:
        form = EmpruntForm()

    context = {
        'form': form
    }
    return render(request, 'emprunts/add.html', context)


def ajouter_enseignant(request):
    if request.method == 'POST':
        form = EnseignantForm(request.POST)
        if form.is_valid():
            enseignant = form.save(commit=False)  # Enregistre l'enseignant dans une instance non sauvegardée
            nom = enseignant.nom

            # Vérification si l'enseignant existe déjà dans la base de données
            if Enseignant.objects.filter(nom=nom).exists():
                form.add_error('nom', 'Cet enseignant existe déjà.')
            else:
                enseignant.save()  # Sauvegarde l'enseignant dans la base de données
                messages.success(request, "Enseignant ajouté avec succès.")  # Message de confirmation
                # Rediriger vers une autre page après avoir ajouté l'enseignant
                return redirect('enseignants')
        else:
            messages.error(request, "Erreur lors de la saisie du formulaire.")
    else:
        form = EnseignantForm()

    context = {
        'form': form,
    }
    return render(request, 'enseignants/add.html', context)

def ajouter_accessoire(request):
    if request.method == 'POST':
        form = AccessoireForm(request.POST)
        if form.is_valid():
            accessoire = form.save(commit=False)  # Enregistre l'enseignant dans une instance non sauvegardée
            nom = accessoire.nom

            # Vérification si l'enseignant existe déjà dans la base de données
            if Accessoire.objects.filter(nom=nom).exists():
                form.add_error('nom', 'Cet accessoire existe déjà.')
            else:
                accessoire.save()  # Sauvegarde l'enseignant dans la base de données
                messages.success(request, "Accessoire ajouté avec succès.")  # Message de confirmation
                # Rediriger vers une autre page après avoir ajouté l'enseignant
                return redirect('accessoires')
        else:
            messages.error(request, "Erreur lors de la saisie du formulaire.")
    else:
        form = AccessoireForm()

    context = {
        'form': form,
    }
    return render(request, 'accessoires/add.html', context)
def ajouter_materiel(request):
    if request.method == 'POST':
        form = MaterielForm(request.POST)
        if form.is_valid():
            materiel = form.save(commit=False)
            nom = materiel.nom

            if Materiel.objects.filter(nom=nom).exists():
                form.add_error('nom', 'Ce matériel existe déjà.')
            else:
                possesseur = materiel.possesseur
                if possesseur is None:
                    # Vérifier si la salle existe
                    salle, created = Salle.objects.get_or_create(numero='001')
                    materiel.salle = salle

                materiel.save()
                accessoires = form.cleaned_data.get('accessoires')
                if accessoires:
                    materiel.accessoires.set(accessoires)

                messages.success(request, "Matériel ajouté avec succès.")
                return redirect('materiels')
        else:
            messages.error(request, "Erreur lors de la saisie du formulaire.")
    else:
        form = MaterielForm()

    context = {
        'form': form,
    }
    return render(request, 'materiels/add.html', context)


def supprimer_salle(request, salle_id):
    salle = get_object_or_404(Salle, id=salle_id)

    if request.method == 'POST':
        salle.delete()
        messages.success(request, "Salle supprimée avec succès.")
        return redirect('salles')

    context = {
        'salle': salle
    }
    return render(request, 'salles/delete.html', context)


def supprimer_enseignant(request, enseignant_id):
    enseignant = get_object_or_404(Enseignant, id=enseignant_id)

    if request.method == 'POST':
        enseignant.delete()
        messages.success(request, "Enseignant supprimée avec succès.")
        return redirect('enseignants')

    context = {
        'enseignant': enseignant
    }
    return render(request, 'enseignants/delete.html', context)

def supprimer_accessoire(request, accessoire_id):
    accessoire = get_object_or_404(Accessoire, id=accessoire_id)

    if request.method == 'POST':
        accessoire.delete()
        messages.success(request, "Accessoire supprimée avec succès.")
        return redirect('accessoires')

    context = {
        'accessoire': accessoire
    }
    return render(request, 'accessoires/delete.html', context)


def supprimer_materiel(request, materiel_id):
    materiel = get_object_or_404(Materiel, id=materiel_id)

    if request.method == 'POST':
        materiel.delete()
        messages.success(request, "Matériel supprimée avec succès.")
        return redirect('materiels')

    context = {
        'materiel': materiel
    }
    return render(request, 'materiels/delete.html', context)


def supprimer_emprunt(request, emprunt_id):
    emprunt = get_object_or_404(ChangementPossesseur, id=emprunt_id)

    if request.method == 'POST':
        emprunt.delete()
        messages.success(request, "Emprunt supprimée avec succès.")
        return redirect('emprunts')

    context = {
        'emprunt': emprunt
    }
    return render(request, 'emprunts/delete.html', context)


def modifier_emprunt(request, emprunt_id):
    emprunt = get_object_or_404(ChangementPossesseur, id=emprunt_id)

    if request.method == 'POST':
        form = EmpruntForm(request.POST, instance=emprunt)
        if form.is_valid():
            form.save()
            emprunt.etat = form.cleaned_data['etat_accessoires']
            emprunt.save()
            materiel = emprunt.materiel  # Obtenir l'instance de Materiel

            # Mettre à jour les propriétés de l'instance
            materiel.possesseur = emprunt.nouveau_possesseur
            materiel.save()  # Appeler la méthode save() sur l'instance de Materiel
            if emprunt.accessoires_presents:
                # Récupérer le matériel lié à l'emprunt
                materiel = emprunt.materiel

                # Mettre à jour l'état des accessoires liés au matériel
                accessoires = get_accessoires(materiel.id)

                for accessoire in accessoires:
                    logger.info(accessoire.id)
                    accessoire.etat = form.cleaned_data['etat_accessoires']
                    accessoire.save()
            messages.success(request, "Emprunt modifié avec succès.")
            return redirect('emprunts')
        else:
            messages.error(request, "Erreur lors de la saisie du formulaire.")
    else:
        form = EmpruntForm(instance=emprunt)

    context = {
        'form': form,
        'emprunt': emprunt
    }
    return render(request, 'emprunts/edit.html', context)


def modifier_salle(request, salle_id):
    salle = get_object_or_404(Salle, id=salle_id)

    if request.method == 'POST':
        form = SalleForm(request.POST, instance=salle)
        if form.is_valid():
            form.save()
            messages.success(request, "Salle modifié avec succès.")
            return redirect('salles')
        else:
            messages.error(request, "Erreur lors de la saisie du formulaire.")
    else:
        form = SalleForm(instance=salle)

    context = {
        'form': form,
        'salle': salle
    }
    return render(request, 'salles/edit.html', context)


def modifier_enseignant(request, enseignant_id):
    enseignant = get_object_or_404(Enseignant, id=enseignant_id)

    if request.method == 'POST':
        form = EnseignantForm(request.POST, instance=enseignant)
        if form.is_valid():
            form.save()
            messages.success(request, "Enseignant modifié avec succès.")
            return redirect('enseignants')
        else:
            messages.error(request, "Erreur lors de la saisie du formulaire.")
    else:
        form = EnseignantForm(instance=enseignant)

    context = {
        'form': form,
        'enseignant': enseignant
    }
    return render(request, 'enseignants/edit.html', context)

def modifier_accessoire(request, accessoire_id):
    accessoire = get_object_or_404(Accessoire, id=accessoire_id)

    if request.method == 'POST':
        form = AccessoireForm(request.POST, instance=accessoire)
        if form.is_valid():
            form.save()
            messages.success(request, "Accessoire modifié avec succès.")
            return redirect('accessoires')
        else:
            messages.error(request, "Erreur lors de la saisie du formulaire.")
    else:
        form = AccessoireForm(instance=accessoire)

    context = {
        'form': form,
        'accessoire': accessoire
    }
    return render(request, 'accessoires/edit.html', context)

def modifier_materiel(request, materiel_id):
    materiel = get_object_or_404(Materiel, id=materiel_id)

    if request.method == 'POST':
        form = MaterielForm(request.POST, instance=materiel)
        if form.is_valid():
            materiel = form.save()

            possesseur = materiel.possesseur
            if possesseur is None:
                # Vérifier si la salle existe
                salle, created = Salle.objects.get_or_create(numero='001')
                materiel.salle = salle

            # Gérer les accessoires associés au matériel
            accessoires = form.cleaned_data.get('accessoires')
            materiel.accessoires.set(accessoires)
            materiel.save()

            messages.success(request, "Matériel modifié avec succès.")
            return redirect('materiels')
        else:
            messages.error(request, "Erreur lors de la saisie du formulaire.")
    else:
        form = MaterielForm(instance=materiel)

    context = {
        'form': form,
        'materiel': materiel
    }
    return render(request, 'materiels/edit.html', context)
