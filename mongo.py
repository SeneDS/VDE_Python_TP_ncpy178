
from pymongo import MongoClient
import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Configuration MongoDB
MONGO_URI = st.secrets[MONGO_URI]  # Assurez-vous d'ajouter l'URI dans Streamlit Cloud ou en local
DB_NAME = "contacts_db"
COLLECTION_NAME = "contacts"

# Connexion à MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

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

# Ajouter un contact
def ajouter_contact(contact):
    """Ajoute un contact dans MongoDB."""
    if collection.find_one({"email": contact.email}):
        st.warning("Un contact avec cet email existe déjà.")
    else:
        collection.insert_one(contact.to_dict())
        st.success("Contact ajouté avec succès.")

# Afficher les contacts
def afficher_contacts():
    """Récupère tous les contacts depuis MongoDB."""
    return list(collection.find({}, {"_id": 0}))

# Rechercher un contact
def rechercher_contact(email):
    """Recherche un contact par email."""
    return collection.find_one({"email": email}, {"_id": 0})

# Supprimer un contact
def supprimer_contact(email):
    """Supprime un contact par email."""
    result = collection.delete_one({"email": email})
    if result.deleted_count > 0:
        st.success("Contact supprimé avec succès.")
    else:
        st.warning("Aucun contact trouvé avec cet email.")

# Streamlit Application
def main():
    st.title("Gestionnaire de Contacts - MongoDB")

    menu = ["Afficher Contacts", "Ajouter Contact", "Rechercher Contact", "Supprimer Contact"]
    choix = st.sidebar.selectbox("Menu", menu)

    if choix == "Afficher Contacts":
        st.subheader("Liste des Contacts")
        contacts = afficher_contacts()
        if contacts:
            st.table(contacts)
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
                ajouter_contact(contact)
            else:
                st.warning("Veuillez remplir tous les champs.")

    elif choix == "Rechercher Contact":
        st.subheader("Rechercher un Contact")
        email = st.text_input("Email du contact à rechercher")
        if st.button("Rechercher"):
            contact = rechercher_contact(email)
            if contact:
                st.json(contact)
            else:
                st.warning("Aucun contact trouvé avec cet email.")

    elif choix == "Supprimer Contact":
        st.subheader("Supprimer un Contact")
        email = st.text_input("Email du contact à supprimer")
        if st.button("Supprimer"):
            supprimer_contact(email)

if __name__ == "__main__":
    main()
