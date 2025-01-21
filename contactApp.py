#=======================================================================================================================
import firebase_admin
from firebase_admin import credentials, db
import streamlit as st
import pandas as pd
import os


from firebase_admin import db


# Charger les credentials Firebase depuis l'environnement
firebase_credentials_json = os.getenv("FIREBASE_CREDENTIALS")

if not firebase_credentials_json:
    raise EnvironmentError("La variable d'environnement 'FIREBASE_CREDENTIALS' est introuvable.")

try:
    # Convertir la chaîne JSON en dictionnaire Python
    firebase_credentials = json.loads(firebase_credentials_json)
    
    # Restaurer les sauts de ligne dans la clé privée
    firebase_credentials["private_key"] = firebase_credentials["private_key"].replace("\\n", "\n")
    
    # Initialiser Firebase si ce n'est pas déjà fait
    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_credentials)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://vde-pythondata-9211c-default-rtdb.europe-west1.firebasedatabase.app/'
        })
except json.JSONDecodeError:
    raise ValueError("Les credentials Firebase sont mal formatés.")
except Exception as e:
    raise RuntimeError(f"Erreur lors de l'initialisation de Firebase : {e}")






# Classe Contact
class Contact:
    def __init__(self, nom, prenom, email, telephone):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.telephone = telephone

    def to_dict(self):
        return {
            "nom": self.nom,
            "prenom": self.prenom,
            "email": self.email,
            "telephone": self.telephone
        }


#Classe  Gestionnaire de Contacts avec Firebase
class GestionnaireContact:
    def __init__(self):
        self.ref = db.reference("contacts")

    def ajouter_contact(self, contact):
        """Ajoute un contact dans Firebase."""
        contacts = self.ref.order_by_child("email").equal_to(contact.email).get()
        if contacts:
            return False  # Contact déjà existant
        self.ref.push(contact.to_dict())
        return True

    def afficher_contacts(self):
        """Récupère tous les contacts de Firebase."""
        return self.ref.get()

    def rechercher_contact(self, email):
        """Recherche un contact par email."""
        contacts = self.ref.order_by_child("email").equal_to(email).get()
        return next(iter(contacts.values()), None)

    def modifier_contact(self, email, nouveau_contact):
        """Modifie un contact existant."""
        contacts = self.ref.order_by_child("email").equal_to(email).get()
        if not contacts:
            return False
        contact_key = next(iter(contacts))
        self.ref.child(contact_key).update(nouveau_contact.to_dict())
        return True

    def supprimer_contact(self, email):
        """Supprime un contact par email."""
        contacts = self.ref.order_by_child("email").equal_to(email).get()
        if not contacts:
            return False
        contact_key = next(iter(contacts))
        self.ref.child(contact_key).delete()
        return True

    def importer_contacts(self, fichier_importe):
        """Importe des contacts depuis un fichier chargé via Streamlit."""
        lignes_ajoutees = 0
        try:
            # Lire le contenu du fichier importé
            contenu = fichier_importe.read().decode("utf-8")
            lignes = contenu.splitlines()

            # Vérifier la structure du fichier
            if not lignes or len(lignes[0].strip().split(",")) != 4:
                st.error("Le fichier doit contenir 4 colonnes : Nom, Prénom, Email, Téléphone.")
                return 0

            for ligne in lignes[1:]:  # Ignore l'en-tête
                valeurs = ligne.strip().split(",")

                # Vérifier si la ligne contient exactement 4 colonnes
                if len(valeurs) != 4:
                    st.warning(f"Ligne ignorée : {ligne} (Format incorrect)")
                    continue

                nom, prenom, email, telephone = valeurs

                # Vérifier si les champs essentiels sont remplis
                if not nom or not email or not telephone:
                    st.warning(f"Ligne ignorée : {ligne} (Nom, Email ou Téléphone manquant)")
                    continue

                # Ajouter le contact à Firebase
                contact = Contact(nom, prenom if prenom else "N/A", email, telephone)
                if self.ajouter_contact(contact):
                    lignes_ajoutees += 1

            return lignes_ajoutees
        except Exception as e:
            st.error(f"Erreur lors de l'importation : {e}")
            return 0


    def exporter_contacts(self):
        """Génère un contenu CSV pour les contacts."""
        contacts = self.afficher_contacts()
        contenu = "Nom,Prénom,Email,Téléphone\n"
        if contacts:
            for key, contact in contacts.items():
                contenu += f"{contact['nom']},{contact['prenom']},{contact['email']},{contact['telephone']}\n"
        return contenu


############################################## Streamlit ##############################################################
def main():
    st.title("Gestionnaire de Contacts avec Firebase")
    gestionnaire = GestionnaireContact()

    menu = ["1. Afficher Contacts", "2. Ajouter Contact", "3. Rechercher Contact", "4. Modifier Contact", "5. Supprimer Contact", "6. Importer Contacts", "7. Exporter Contacts",  "8. Quitter"]
    choix = st.sidebar.selectbox("Menu", menu)


    if choix == "1. Afficher Contacts":
        st.subheader("Liste des Contacts")
        contacts = gestionnaire.afficher_contacts()
        if contacts:
            df = pd.DataFrame(contacts.values())
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
            contacts = gestionnaire.afficher_contacts()
            if contacts:
                df = pd.DataFrame(contacts.values())
                st.dataframe(df)


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











































#import firebase_admin
#from firebase_admin import credentials

#cred = credentials.Certificate("path/to/serviceAccountKey.json")
#firebase_admin.initialize_app(cred)
