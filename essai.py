import os
import pandas as pd
import streamlit as st


# Classe Contact
class Contact:
    def __init__(self, nom, prenom, email, telephone):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.telephone = telephone

    def __str__(self):
        return f"Nom: {self.nom}, Prénom: {self.prenom}, Email: {self.email}, Téléphone: {self.telephone}"


# Gestionnaire des Contacts
class GestionnaireContact:
    def __init__(self):
        self.contacts = []
        self.fichier = "contacts.txt"
        self.charger_contacts()

    def ajouter_contact(self, contact):
        """Ajoute un contact s'il n'est pas déjà dans la liste."""
        if not any(c.email == contact.email for c in self.contacts):
            self.contacts.append(contact)
            self.sauvegarder_contacts()
            return True
        return False

    def importer_contacts(self, fichier_importe):
        """Importe des contacts depuis un fichier chargé via Streamlit."""
        try:
            contenu = fichier_importe.read().decode("utf-8")
            lignes = contenu.splitlines()
            lignes_ajoutees = 0
            for ligne in lignes:
                valeurs = ligne.strip().split(",")
                if len(valeurs) == 4:
                    nom, prenom, email, telephone = valeurs
                    if self.ajouter_contact(Contact(nom, prenom, email, telephone)):
                        lignes_ajoutees += 1
            return lignes_ajoutees
        except Exception as e:
            st.error(f"Erreur lors de l'importation : {e}")

    def exporter_contacts(self, chemin_fichier):
        """Exporte les contacts dans un fichier texte."""
        try:
            with open(chemin_fichier, "w") as f:
                header = f"{'Nom':<20}{'Prénom':<20}{'Email':<30}{'Téléphone':<15}\n"
                f.write(header)
                f.write("-" * len(header) + "\n")
                for contact in self.contacts:
                    ligne = f"{contact.nom:<20}{contact.prenom:<20}{contact.email:<30}{contact.telephone:<15}\n"
                    f.write(ligne)
            return True
        except Exception as e:
            st.error(f"Erreur lors de l'exportation : {e}")
            return False

    def contacts_en_dataframe(self):
        """Convertit la liste des contacts en DataFrame."""
        data = [
            {"Nom": contact.nom, "Prénom": contact.prenom, "Email": contact.email, "Téléphone": contact.telephone}
            for contact in self.contacts
        ]
        return pd.DataFrame(data)

    def rechercher_contact(self, email):
        """Recherche un contact par email."""
        for contact in self.contacts:
            if contact.email == email:
                return contact
        return None

    def modifier_contact(self, email, nouveau_contact):
        """Modifie un contact en remplaçant ses informations."""
        for i, contact in enumerate(self.contacts):
            if contact.email == email:
                self.contacts[i] = nouveau_contact
                self.sauvegarder_contacts()
                return True
        return False


    def supprimer_contact(self, email):
        """Supprime un contact par email."""
        contact = self.rechercher_contact(email)
        if contact:
            self.contacts.remove(contact)
            self.sauvegarder_contacts()
            return True
        return False

    def sauvegarder_contacts(self):
        """Sauvegarde les contacts dans un fichier texte."""
        with open(self.fichier, "w") as f:
            for contact in self.contacts:
                ligne = f"{contact.nom},{contact.prenom},{contact.email},{contact.telephone}\n"
                f.write(ligne)

    def charger_contacts(self):
        """Charge les contacts depuis un fichier texte."""
        if os.path.exists(self.fichier):
            with open(self.fichier, "r") as f:
                for ligne in f:
                    valeurs = ligne.strip().split(",")
                    if len(valeurs) == 4:
                        nom, prenom, email, telephone = valeurs
                        self.contacts.append(Contact(nom, prenom, email, telephone))





# Application Streamlit
def main():
    st.title("Gestionnaire de Contacts")
    gestionnaire = GestionnaireContact()

    menu = ["Afficher Contacts", "Ajouter Contact", "Importer Contacts", "Exporter Contacts", "Rechercher Contact", "Modifier Contact", "Supprimer Contact", "Quitter"]
    choix = st.sidebar.selectbox("Menu", menu)

    if choix == "Afficher Contacts":
        st.subheader("Liste des Contacts")
        df = gestionnaire.contacts_en_dataframe()
        if not df.empty:
            st.dataframe(df)
        else:
            st.info("Aucun contact disponible.")

    elif choix == "Ajouter Contact":
        st.subheader("Ajouter un Nouveau Contact")
        with st.form("ajout_contact"):
            nom = st.text_input("Nom")
            prenom = st.text_input("Prénom")
            email = st.text_input("Email")
            telephone = st.text_input("Téléphone")
            submitted = st.form_submit_button("Ajouter")

        if submitted:
            if nom and prenom and email and telephone:
                contact = Contact(nom, prenom, email, telephone)
                if gestionnaire.ajouter_contact(contact):
                    st.success(f"Contact {nom} ajouté avec succès.")
                else:
                    st.warning(f"Le contact avec l'email {email} existe déjà.")
            else:
                st.warning("Veuillez remplir tous les champs.")

    elif choix == "Importer Contacts":
        st.subheader("Importer Contacts depuis un Fichier")
        fichier_import = st.file_uploader("Choisissez un fichier CSV ou TXT", type=["txt", "csv"])

        if fichier_import is not None:
            lignes_ajoutees = gestionnaire.importer_contacts(fichier_import)
            st.success(f"{lignes_ajoutees} contacts importés avec succès.")
            df = gestionnaire.contacts_en_dataframe()
            st.dataframe(df)

    elif choix == "Exporter Contacts":
        st.subheader("Exporter les Contacts")
        chemin_fichier = st.text_input("Nom du fichier d'export (ex. export_contacts.txt)")
        if st.button("Exporter"):
            if chemin_fichier:
                if gestionnaire.exporter_contacts(chemin_fichier):
                    st.success(f"Contacts exportés dans {chemin_fichier} avec succès.")
            else:
                st.warning("Veuillez entrer un nom de fichier.")

    elif choix == "Rechercher Contact":
        st.subheader("Rechercher un Contact")
        email = st.text_input("Email du contact à rechercher")
        if st.button("Rechercher"):
            contact = gestionnaire.rechercher_contact(email)
            if contact:
                st.write(contact)
            else:
                st.warning("Aucun contact trouvé avec cet email.")

    elif choix == "Modifier Contact":
        st.subheader("Modifier un Contact")
        email = st.text_input("Email du contact à modifier")
        if st.button("Rechercher pour Modifier"):
            contact = gestionnaire.rechercher_contact(email)
            if contact:
                with st.form("form_modifier"):
                    nouveau_nom = st.text_input("Nouveau Nom", value=contact.nom)
                    nouveau_prenom = st.text_input("Nouveau Prénom", value=contact.prenom)
                    nouvel_email = st.text_input("Nouvel Email", value=contact.email)
                    nouveau_telephone = st.text_input("Nouveau Téléphone", value=contact.telephone)
                    submit = st.form_submit_button("Modifier")
                    if submit:
                        nouveau_contact = Contact(nouveau_nom, nouveau_prenom, nouvel_email, nouveau_telephone)
                        gestionnaire.modifier_contact(email, nouveau_contact)
                        st.success(f"Contact {email} modifié avec succès.")

    elif choix == "Supprimer Contact":
        st.subheader("Supprimer un Contact")
        email = st.text_input("Email du contact à supprimer")
        if st.button("Supprimer"):
            if gestionnaire.supprimer_contact(email):
                st.success(f"Contact avec l'email {email} supprimé avec succès.")
            else:
                st.warning("Aucun contact trouvé avec cet email.")

    elif choix == "Quitter":
        st.subheader("Quitter l'application")
        st.write("Merci d'avoir utilisé le gestionnaire de contacts. À bientôt !")


if __name__ == "__main__":
    main()


#=======================================================================================================================
#Voir le script github pour la recherrche de contact
#Choix du format d'export et d'import
#Possibilité de connecter l'application à une base de données.