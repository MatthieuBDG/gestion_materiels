from django.core.management.base import BaseCommand
from materiels.models import Enseignant, Salle, Materiel, Accessoire, ChangementPossesseur
from datetime import date


class Command(BaseCommand):
    help = 'Insérer des données dans la base de données'

    def handle(self, *args, **kwargs):

        # Insérer les enseignants
        enseignants = ['Pierre Dubois', 'Philippe Durand', 'Thierry Dupré', 'Sophie Dupuy']
        for nom in enseignants:
            enseignant, _ = Enseignant.objects.get_or_create(nom=nom)

        # Insérer les salles
        salles = ['001', '101', '102', '103', '104', '105', '201', '202', '203', '204', '205', '301', '302', '303',
                  '304', '305']
        for numero in salles:
            salle, _ = Salle.objects.get_or_create(numero=numero)

        # Insérer les matériels
        materiels = [
            {'nom': 'smartphone', 'budget_annuel': 500.00, 'budget_projets': 0.00,
             'budget_financements_exceptionnels': 0.00, 'acheteur': 'Pierre Dubois', 'mandant': None,
             'proprietaire': 'Pierre Dubois', 'possesseur': None, 'salle': '001',
             'accessoires': ['Chargeur', 'Câble USB']},
            {'nom': 'smartphone', 'budget_annuel': 500.00, 'budget_projets': 0.00,
             'budget_financements_exceptionnels': 0.00, 'acheteur': 'Pierre Dubois', 'mandant': None,
             'proprietaire': 'Pierre Dubois', 'possesseur': 'Philippe Durand', 'salle': '104',
             'accessoires': ['Chargeur', 'Câble USB']},
            {'nom': 'tablette', 'budget_annuel': 800.00, 'budget_projets': 0.00,
             'budget_financements_exceptionnels': 0.00, 'acheteur': 'Philippe Durand', 'mandant': None,
             'proprietaire': 'Pierre Dubois', 'possesseur': 'Thierry Dupré', 'salle': '101',
             'accessoires': ['Chargeur', 'Câble USB']},
            {'nom': 'tablette', 'budget_annuel': 800.00, 'budget_projets': 0.00,
             'budget_financements_exceptionnels': 0.00, 'acheteur': 'Philippe Durand', 'mandant': None,
             'proprietaire': 'Pierre Dubois', 'possesseur': 'Philippe Durand', 'salle': '201',
             'accessoires': ['Chargeur', 'Câble USB']},
            {'nom': 'écran', 'budget_annuel': 1000.00, 'budget_projets': 0.00,
             'budget_financements_exceptionnels': 0.00, 'acheteur': None, 'mandant': 'Philippe Durand',
             'proprietaire': 'Thierry Dupré', 'possesseur': 'Philippe Durand', 'salle': '102',
             'accessoires': ['Câble d’alimentation', 'Câble HDMI']},
            {'nom': 'écran', 'budget_annuel': 1000.00, 'budget_projets': 0.00,
             'budget_financements_exceptionnels': 0.00, 'acheteur': None, 'mandant': 'Philippe Durand',
             'proprietaire': 'Thierry Dupré', 'possesseur': None, 'salle': '001',
             'accessoires': ['Câble d’alimentation', 'Câble HDMI']},
            {'nom': 'vidéo-projecteur', 'budget_annuel': 1500.00, 'budget_projets': 0.00,
             'budget_financements_exceptionnels': 0.00, 'acheteur': None, 'mandant': 'Philippe Durand',
             'proprietaire': 'Sophie Dupuy', 'possesseur': 'Sophie Dupuy', 'salle': '103',
             'accessoires': ['Câble d’alimentation', 'Câble HDMI']},
            {'nom': 'vidéo-projecteur', 'budget_annuel': 1500.00, 'budget_projets': 0.00,
             'budget_financements_exceptionnels': 0.00, 'acheteur': None, 'mandant': 'Philippe Durand',
             'proprietaire': 'Sophie Dupuy', 'possesseur': 'Philippe Durand', 'salle': '302',
             'accessoires': ['Câble d’alimentation', 'Câble HDMI']},
            {'nom': 'vidéo-projecteur', 'budget_annuel': 1500.00, 'budget_projets': 0.00,
             'budget_financements_exceptionnels': 0.00, 'acheteur': None, 'mandant': 'Philippe Durand',
             'proprietaire': 'Sophie Dupuy', 'possesseur': None, 'salle': '001',
             'accessoires': ['Câble d’alimentation', 'Câble HDMI']},
            {'nom': 'pointeur laser', 'budget_annuel': 50.00, 'budget_projets': 0.00,
             'budget_financements_exceptionnels': 0.00, 'acheteur': 'Pierre Dubois', 'mandant': None,
             'proprietaire': 'Philippe Durand', 'possesseur': 'Sophie Dupuy', 'salle': '202', 'accessoires': ['Piles']},
            {'nom': 'pointeur laser', 'budget_annuel': 50.00, 'budget_projets': 0.00,
             'budget_financements_exceptionnels': 0.00, 'acheteur': 'Pierre Dubois', 'mandant': None,
             'proprietaire': 'Thierry Dupré', 'possesseur': 'Pierre Dubois', 'salle': '203', 'accessoires': ['Piles']},
            {'nom': 'pointeur laser', 'budget_annuel': 50.00, 'budget_projets': 0.00,
             'budget_financements_exceptionnels': 0.00, 'acheteur': 'Pierre Dubois', 'mandant': None,
             'proprietaire': 'Philippe Durand', 'possesseur': 'Philippe Durand', 'salle': '202',
             'accessoires': ['Piles']}
        ]
        for m in materiels:
            acheteur = Enseignant.objects.get(nom=m['acheteur']) if m['acheteur'] else None
            mandant = Enseignant.objects.get(nom=m['mandant']) if m['mandant'] else None
            proprietaire = Enseignant.objects.get(nom=m['proprietaire'])
            possesseur = Enseignant.objects.get(nom=m['possesseur']) if m['possesseur'] else None

            salle = Salle.objects.get(numero=m['salle'])

            if not Materiel.objects.filter(nom=m['nom'], proprietaire=proprietaire,
                                           possesseur=possesseur, salle=salle).exists():
                materiel = Materiel.objects.create(nom=m['nom'], budget_annuel=m['budget_annuel'],
                                                   budget_projets=m['budget_projets'],
                                                   budget_financements_exceptionnels=m[
                                                       'budget_financements_exceptionnels'], acheteur=acheteur,
                                                   mandant=mandant,
                                                   proprietaire=proprietaire, possesseur=possesseur,
                                                   salle=salle)
                for accessoire_name in m.get('accessoires', []):
                    accessoire = Accessoire.objects.create(nom=accessoire_name)
                    materiel.accessoires.add(accessoire)

        self.stdout.write(self.style.SUCCESS('Données insérées avec succès.'))
