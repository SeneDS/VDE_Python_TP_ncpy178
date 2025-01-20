1. Importations
import os
import pandas as pd
import streamlit as st
os : Permet d'interagir avec le système de fichiers pour vérifier l'existence de fichiers et manipuler les chemins.
pandas : Utilisé pour créer et manipuler des tableaux de données (DataFrames), qui sont utilisés pour afficher les contacts.
streamlit : Framework utilisé pour créer une interface web interactive pour votre application.
2. Classe Contact
class Contact:
    def __init__(self, nom, prenom, email, telephone):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.telephone = telephone

    def __str__(self):
        return f"Nom: {self.nom}, Prénom: {self.prenom}, Email: {self.email}, Téléphone: {self.telephone}"
Cette classe représente un contact avec quatre attributs :
nom : Le nom de la personne.
prenom : Le prénom de la personne.
email : L'adresse email unique du contact.
telephone : Le numéro de téléphone du contact.
La méthode __str__ permet d'afficher un contact sous forme de chaîne lisible.
3. Classe GestionnaireContact
Cette classe gère les opérations sur la liste de contacts.

Constructeur : __init__

    def __init__(self):
        self.contacts = []
        self.fichier = "contacts.txt"
        self.charger_contacts()
Initialise une liste vide pour les contacts.
Charge les contacts depuis un fichier contacts.txt s'il existe.
Ajout de contact

    def ajouter_contact(self, contact):
        if not any(c.email == contact.email for c in self.contacts):
            self.contacts.append(contact)
            self.sauvegarder_contacts()
            return True
        return False
Vérifie si l'email du contact est déjà présent dans la liste (pour éviter les doublons).
Ajoute le contact et sauvegarde la liste mise à jour dans un fichier.
Importer des contacts

    def importer_contacts(self, fichier_importe):
        ...
Lit un fichier texte ou CSV fourni par l'utilisateur via Streamlit.
Ajoute chaque ligne en tant que contact, en supposant que chaque ligne a le format nom,prenom,email,telephone.
Exporter des contacts

    def exporter_contacts(self, chemin_fichier):
        ...
Exporte la liste des contacts dans un fichier texte formaté avec des colonnes alignées.
Rechercher un contact

    def rechercher_contact(self, email):
        ...
Recherche un contact par son email.
Modifier un contact

    def modifier_contact(self, email, nom=None, prenom=None, new_email=None, telephone=None):
        ...
Permet de mettre à jour les informations d'un contact existant, en recherchant par email.
Supprimer un contact

    def supprimer_contact(self, email):
        ...
Supprime un contact de la liste en utilisant son email.
Sauvegarder et charger des contacts

    def sauvegarder_contacts(self):
        ...
Sauvegarde la liste des contacts dans un fichier texte.
    def charger_contacts(self):
        ...
Charge les contacts depuis un fichier texte existant (contacts.txt).
4. Application Streamlit

 ````
def main():
    st.title("Gestionnaire de Contacts")
    gestionnaire = GestionnaireContact()
    ...
```

main() : Fonction principale où l'interface utilisateur est définie.
Menu

    menu = ["Afficher Contacts", "Ajouter Contact", "Importer Contacts", "Exporter Contacts", "Rechercher Contact", "Modifier Contact", "Supprimer Contact", "Quitter"]
    choix = st.sidebar.selectbox("Menu", menu)
Crée une barre latérale avec les différentes options du menu.
Afficher les contacts

    if choix == "Afficher Contacts":
        df = gestionnaire.contacts_en_dataframe()
        st.dataframe(df)
Affiche la liste des contacts sous forme d'un tableau interactif.
Ajouter un contact

    elif choix == "Ajouter Contact":
        with st.form("ajout_contact"):
            ...
        if submitted:
            gestionnaire.ajouter_contact(contact)
Utilise un formulaire pour ajouter un nouveau contact.
Importer des contacts

    elif choix == "Importer Contacts":
        fichier_import = st.file_uploader("Choisissez un fichier CSV ou TXT", type=["txt", "csv"])
        gestionnaire.importer_contacts(fichier_import)
Permet de charger un fichier contenant des contacts.
Exporter des contacts

    elif choix == "Exporter Contacts":
        chemin_fichier = st.text_input("Nom du fichier d'export")
        gestionnaire.exporter_contacts(chemin_fichier)
Exporte la liste des contacts dans un fichier texte.
Rechercher un contact

    elif choix == "Rechercher Contact":
        email = st.text_input("Email du contact à rechercher")
        gestionnaire.rechercher_contact(email)
Recherche un contact en fonction de son email.
Modifier un contact

    elif choix == "Modifier Contact":
        email = st.text_input("Email du contact à modifier")
        gestionnaire.modifier_contact(email, nom, prenom, new_email, telephone)
Permet de modifier un contact.
Supprimer un contact

    elif choix == "Supprimer Contact":
        email = st.text_input("Email du contact à supprimer")
        gestionnaire.supprimer_contact(email)
Supprime un contact en fonction de son email.
Quitter l'application

    elif choix == "Quitter":
        st.subheader("Quitter l'application")
Affiche un message pour indiquer la fin de l'application.
Résumé des fonctionnalités
CRUD : Permet d'ajouter, afficher, modifier et supprimer des contacts.
Import/Export : Gestion des fichiers de contacts.
Recherche : Trouver des contacts rapidement.
Interface intuitive : Utilise Streamlit pour une expérience interactive.