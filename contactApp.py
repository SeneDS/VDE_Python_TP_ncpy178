import streamlit as st
import os

# 1. Classe Contact
class Contact:
    def __init__(self, nom, prenom, email, telephone):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.telephone = telephone

    def __str__(self):
        return f"Nom: {self.nom}, Prénom: {self.prenom}, Email: {self.email}, Téléphone: {self.telephone}"


# 2. Gestion des Contacts en Mémoire
class GestionnaireContact:
    def __init__(self):
        self.contacts = []
        self.fichier = "contacts.txt"
        self.charger_contacts()

    def ajouter_contact(self, contact):
        self.contacts.append(contact)

    def afficher_contacts(self):
        return self.contacts

    def rechercher_contact(self, nom):
        for contact in self.contacts:
            if contact.nom.lower() == nom.lower():
                return contact
        return None

    def modifier_contact(self, nom, nouveau_contact):
        for i, contact in enumerate(self.contacts):
            if contact.nom.lower() == nom.lower():
                self.contacts[i] = nouveau_contact
                return True
        return False

    def supprimer_contact(self, nom):
        for contact in self.contacts:
            if contact.nom.lower() == nom.lower():
                self.contacts.remove(contact)
                return True
        return False

    def sauvegarder_contacts(self):
        with open(self.fichier, "w") as f:
            for contact in self.contacts:
                ligne = f"{contact.nom},{contact.prenom},{contact.email},{contact.telephone}\n"
                f.write(ligne)

    def charger_contacts(self):
        if os.path.exists(self.fichier):
            with open(self.fichier, "r") as f:
                for ligne in f:
                    valeurs = ligne.strip().split(",")
                    if len(valeurs) == 4:
                        nom, prenom, email, telephone = valeurs
                        self.contacts.append(Contact(nom, prenom, email, telephone))

    def importer_contacts(self, fichier):
        """Importe des contacts depuis un fichier texte."""
        lignes_ajoutees = 0
        for ligne in fichier.decode("utf-8").splitlines():
            valeurs = ligne.strip().split(",")
            if len(valeurs) == 4:
                nom, prenom, email, telephone = valeurs
                self.contacts.append(Contact(nom, prenom, email, telephone))
                lignes_ajoutees += 1
        self.sauvegarder_contacts()
        return lignes_ajoutees

    def exporter_contacts_txt(self):
        with open("export_contacts.txt", "w") as f:
            header = f"{'Nom':<20}{'Prénom':<20}{'Email':<30}{'Téléphone':<15}\n"
            f.write(header)
            f.write("-" * len(header) + "\n")
            for contact in self.contacts:
                ligne = f"{contact.nom:<20}{contact.prenom:<20}{contact.email:<30}{contact.telephone:<15}\n"
                f.write(ligne)
        return "export_contacts.txt"


# Initialisation du gestionnaire
gestionnaire = GestionnaireContact()

# Application Streamlit
st.title("Gestionnaire de Contacts")

menu = [
    "Afficher les Contacts",
    "Ajouter un Contact",
    "Rechercher un Contact",
    "Modifier un Contact",
    "Supprimer un Contact",
    "Exporter les Contacts",
    "Importer des Contacts",
     "Quitter l'application",
]
choix = st.sidebar.selectbox("Menu", menu)

if choix == "Afficher les Contacts":
    st.subheader("Liste de Tous les Contacts")
    contacts = gestionnaire.afficher_contacts()
    if contacts:
        for contact in contacts:
            st.text(contact)
    else:
        st.warning("Aucun contact trouvé.")

elif choix == "Ajouter un Contact":
    st.subheader("Ajouter un Nouveau Contact")
    with st.form("form_ajouter"):
        nom = st.text_input("Nom")
        prenom = st.text_input("Prénom")
        email = st.text_input("Email")
        telephone = st.text_input("Téléphone")
        submit = st.form_submit_button("Ajouter")
        if submit:
            if nom and prenom and email and telephone:
                contact = Contact(nom, prenom, email, telephone)
                gestionnaire.ajouter_contact(contact)
                gestionnaire.sauvegarder_contacts()
                st.success(f"Contact {nom} ajouté avec succès.")
            else:
                st.error("Veuillez remplir tous les champs.")

elif choix == "Rechercher un Contact":
    st.subheader("Rechercher un Contact")
    nom = st.text_input("Nom du contact à rechercher")
    if st.button("Rechercher"):
        contact = gestionnaire.rechercher_contact(nom)
        if contact:
            st.success("Contact trouvé :")
            st.text(contact)
        else:
            st.error("Aucun contact trouvé avec ce nom.")

elif choix == "Modifier un Contact":
    st.subheader("Modifier un Contact")
    nom = st.text_input("Nom du contact à modifier")
    if st.button("Rechercher pour Modifier"):
        contact = gestionnaire.rechercher_contact(nom)
        if contact:
            with st.form("form_modifier"):
                nouveau_nom = st.text_input("Nouveau Nom", value=contact.nom)
                nouveau_prenom = st.text_input("Nouveau Prénom", value=contact.prenom)
                nouvel_email = st.text_input("Nouvel Email", value=contact.email)
                nouveau_telephone = st.text_input("Nouveau Téléphone", value=contact.telephone)
                submit = st.form_submit_button("Modifier")
                if submit:
                    nouveau_contact = Contact(nouveau_nom, nouveau_prenom, nouvel_email, nouveau_telephone)
                    gestionnaire.modifier_contact(nom, nouveau_contact)
                    gestionnaire.sauvegarder_contacts()
                    st.success(f"Contact {nom} modifié avec succès.")
        else:
            st.error("Aucun contact trouvé avec ce nom.")

elif choix == "Supprimer un Contact":
    st.subheader("Supprimer un Contact")
    nom = st.text_input("Nom du contact à supprimer")
    if st.button("Supprimer"):
        success = gestionnaire.supprimer_contact(nom)
        if success:
            gestionnaire.sauvegarder_contacts()
            st.success(f"Contact {nom} supprimé avec succès.")
        else:
            st.error("Aucun contact trouvé avec ce nom.")

elif choix == "Exporter les Contacts":
    st.subheader("Exporter les Contacts")
    fichier_export = gestionnaire.exporter_contacts_txt()
    with open(fichier_export, "r") as f:
        st.download_button("Télécharger les Contacts", f, file_name=fichier_export)

elif choix == "Importer des Contacts":
    st.subheader("Importer des Contacts")
    fichier_import = st.file_uploader("Choisissez un fichier de contacts (.txt)", type=["txt"])
    if fichier_import:
        lignes_ajoutees = gestionnaire.importer_contacts(fichier_import.getvalue())
        st.success(f"{lignes_ajoutees} contacts ajoutés avec succès.")

elif choix ==   "Quitter l'application":
    st.subheader("Quitter l'application")
    st.warning("Vous pouvez fermer l'onglet !")
    st.stop()
