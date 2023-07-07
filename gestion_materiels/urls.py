from django.contrib import admin
from django.urls import path
from materiels import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('materiels/', views.materiels, name='materiels'),
    path('accessoires/', views.accessoires, name='accessoires'),
    path('enseignants/', views.enseignants, name='enseignants'),
    path('salles/', views.salles, name='salles'),
    path('emprunts/', views.emprunts, name='emprunts'),

    path('salles/ajouter/', views.ajouter_salle, name='ajouter_salle'),
    path('enseignants/ajouter/', views.ajouter_enseignant, name='ajouter_enseignant'),
    path('materiels/ajouter/', views.ajouter_materiel, name='ajouter_materiel'),
    path('accessoires/ajouter/', views.ajouter_accessoire, name='ajouter_accessoire'),
    path('emprunts/ajouter/', views.ajouter_emprunt, name='ajouter_emprunt'),

    path('salles/supprimer/<int:salle_id>/', views.supprimer_salle, name='supprimer_salle'),
    path('enseignants/supprimer/<int:enseignant_id>/', views.supprimer_enseignant, name='supprimer_enseignant'),
    path('materiels/supprimer/<int:materiel_id>/', views.supprimer_materiel, name='supprimer_materiel'),
    path('accessoires/supprimer/<int:accessoire_id>/', views.supprimer_accessoire, name='supprimer_accessoire'),
    path('emprunts/supprimer/<int:emprunt_id>/', views.supprimer_emprunt, name='supprimer_emprunt'),

    path('salles/modifier/<int:salle_id>/', views.modifier_salle, name='modifier_salle'),
    path('enseignants/modifier/<int:enseignant_id>/', views.modifier_enseignant, name='modifier_enseignant'),
    path('materiels/modifier/<int:materiel_id>/', views.modifier_materiel, name='modifier_materiel'),
    path('accessoires/modifier/<int:accessoire_id>/', views.modifier_accessoire, name='modifier_accessoire'),
    path('emprunts/modifier/<int:emprunt_id>/', views.modifier_emprunt, name='modifier_emprunt'),

    path('get_accessoires/', views.get_accessoires, name='get_accessoires'),
]
