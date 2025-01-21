import streamlit as st
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import pandas as pd

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Configuration Supabase à partir des variables d'environnement
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Créer un client Supabase
@st.cache_resource
def init_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

# Classe Contact
class Contact:
    def __init__(self, nom, prenom, email, telephone):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.telephone = telephone

    def to_dict(self):
        """Convertit l'objet Contact en dictionnaire."""
        return {
            "nom": self.nom,
            "prenom": self.prenom,
            "email": self.email,
            "telephone": self.telephone
        }

# Classe Gestionnaire de Contacts
class GestionnaireContact:
    def __init__(self):
        self.ref = supabase.table("contacts")

    def ajouter_contact(self, contact):
        """Ajoute un contact à Supabase."""
        try:
            contacts = self.ref.select("*").eq("email", contact.email).execute()
            if contacts.data:
                return False  # Contact déjà existant
            self.ref.insert(contact.to_dict()).execute()
            return True
        except Exception as e:
            st.error(f"Erreur lors de l'ajout du contact : {e}")
            return False

    def afficher_contacts(self):
        """Récupère tous les contacts depuis Supabase."""
        try:
            result = self.ref.select("*").execute()
            return result.data
        except Exception as e:
            st.error(f"Erreur lors de la récupération des contacts : {e}")
            return None

    def rechercher_contact(self, email):
        """Recherche un contact par email."""
        try:
            contacts = self.ref.select("*").eq("email", email).execute()
            return next((contact for contact in contacts.data), None)
        except Exception as e:
            st.error(f"Erreur lors de la recherche du contact : {e}")
            return None

    def modifier_contact(self, email, nouveau_contact):
        """Modifie un contact existant."""
        try:
            contacts = self.ref.select("*").eq("email", email).execute()
            if not contacts.data:
                return False
            contact_key = contacts.data[0]['id']
            self.ref.update(nouveau_contact.to_dict()).eq("id", contact_key).execute()
            return True
        except Exception as e:
            st.error(f"Erreur lors de la modification du contact : {e}")
            return False

    def supprimer_contact(self, email):
        """Supprime un contact existant."""
        try:
            contacts = self.ref.select("*").eq("email", email).execute()
            if not contacts.data:
                return False
            contact_key = contacts.data[0]['id']
            self.ref.delete().eq("id", contact_key).execute()
            return True
        except Exception as e:
            st.error(f"Erreur lors de la suppression du contact : {e}")
            return False

    def importer_contacts(self, fichier_importe):
        """Importe des contacts depuis un fichier chargé via Streamlit."""
        lignes_ajoutees = 0
        try:
            contenu = fichier_importe.read().decode("utf-8")
            lignes = contenu.splitlines()

            if not lignes or len(lignes[0].strip().split(",")) != 4:
                st.error("Le fichier doit contenir 4 colonnes : Nom, Prénom, Email, Téléphone.")
                return 0

            for ligne in lignes[1:]:
                valeurs = ligne.strip().split(",")
                if len(valeurs) != 4:
                    st.warning(f"Ligne ignorée : {ligne} (Format incorrect)")
                    continue
                nom, prenom, email, telephone = valeurs
                contact = Contact(nom, prenom if prenom else "N/A", email, telephone)
                if self.ajouter_contact(contact):
                    lignes_ajoutees += 1
            return lignes_ajoutees
        except Exception as e:
            st.error(f"Erreur lors de l'importation des contacts : {e}")
            return 0

    def exporter_contacts(self):
        """Génère un contenu CSV pour l'export des contacts."""
        try:
            contacts = self.afficher_contacts()
            contenu = "Nom,Prénom,Email,Téléphone\n"
            if contacts:
                for contact in contacts:
                    contenu += f"{contact['nom']},{contact['prenom']},{contact['email']},{contact['telephone']}\n"
            return contenu
        except Exception as e:
            st.error(f"Erreur lors de l'exportation des contacts : {e}")
            return ""

############################################## Streamlit ##############################################################
def main():
    st.title("Gestionnaire de Contacts avec Supabase")
    gestionnaire = GestionnaireContact()

    menu = ["1. Afficher Contacts", "2. Ajouter Contact", "3. Rechercher Contact", "4. Modifier Contact", "5. Supprimer Contact", "6. Importer Contacts", "7. Exporter Contacts", "8. Quitter"]
    choix = st.sidebar.selectbox("Menu", menu)

    if choix == "1. Afficher Contacts":
        st.subheader("Liste des Contacts")
        contacts = gestionnaire.afficher_contacts()
        if contacts:
            df = pd.DataFrame(contacts)
            st.dataframe(df)
        else:
            st.info("Aucun contact disponible.")

    elif choix == "2. Ajouter Contact":
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
                    st.warning("Un contact avec cet email existe déjà.")
            else:
                st.warning("Veuillez remplir tous les champs.")

    elif choix == "3. Rechercher Contact":
        st.subheader("Rechercher un Contact")
        email = st.text_input("Email du contact à rechercher")
        if st.button("Rechercher"):
            contact = gestionnaire.rechercher_contact(email)
            if contact:
                st.write(contact)
            else:
                st.warning("Aucun contact trouvé avec cet email.")

    elif choix == "4. Modifier Contact":
        st.subheader("Modifier un Contact")
        email = st.text_input("Email du contact à modifier")
        if st.button("Rechercher pour Modifier"):
            contact = gestionnaire.rechercher_contact(email)
            if contact:
                with st.form("form_modifier"):
                    nouveau_nom = st.text_input("Nouveau Nom", value=contact["nom"])
                    nouveau_prenom = st.text_input("Nouveau Prénom", value=contact["prenom"])
                    nouvel_email = st.text_input("Nouvel Email", value=contact["email"])
                    nouveau_telephone = st.text_input("Nouveau Téléphone", value=contact["telephone"])
                    submit = st.form_submit_button("Modifier")
                    if submit:
                        nouveau_contact = Contact(nouveau_nom, nouveau_prenom, nouvel_email, nouveau_telephone)
                        gestionnaire.modifier_contact(email, nouveau_contact)
                        st.success(f"Contact {email} modifié avec succès.")

    elif choix == "5. Supprimer Contact":
        st.subheader("Supprimer un Contact")
        email = st.text_input("Email du contact à supprimer")
        if st.button("Supprimer"):
            if gestionnaire.supprimer_contact(email):
                st.success(f"Contact avec l'email {email} supprimé avec succès.")
            else:
                st.warning("Aucun contact trouvé avec cet email.")

    elif choix == "6. Importer Contacts":
        st.subheader("Importer Contacts depuis un Fichier")
        fichier_import = st.file_uploader("Choisissez un fichier CSV ou TXT", type=["txt", "csv"])
        if fichier_import is not None:
            lignes_ajoutees = gestionnaire.importer_contacts(fichier_import)
            st.success(f"{lignes_ajoutees} contacts importés avec succès.")

    elif choix == "7. Exporter Contacts":
        st.subheader("Exporter les Contacts")
        contenu = gestionnaire.exporter_contacts()
        st.download_button(
            label="Télécharger les Contacts",
            data=contenu,
            file_name="contacts_export.csv",
            mime="text/csv"
        )

    elif choix == "8. Quitter":
        st.subheader("Quitter l'application")
        st.write("Merci d'avoir utilisé le gestionnaire de contacts. À bientôt !")

if __name__ == "__main__":
    main()
