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
        if not self.contacts:
            print("Aucun contact disponible.")
        for contact in self.contacts:
            print(contact)

    def rechercher_contact(self, nom):
        for contact in self.contacts:
            if contact.nom.lower() == nom.lower():
                return contact
        return None

    def modifier_contact(self, nom):
        contact = self.rechercher_contact(nom)
        if contact:
            print("Contact trouvé :")
            print(contact)
            contact.nom = input("Nouveau nom : ") or contact.nom
            contact.prenom = input("Nouveau prénom : ") or contact.prenom
            contact.email = input("Nouvel email : ") or contact.email
            contact.telephone = input("Nouveau téléphone : ") or contact.telephone
            print("Contact modifié avec succès !")
        else:
            print("Contact introuvable.")

    def supprimer_contact(self, nom):
        contact = self.rechercher_contact(nom)
        if contact:
            self.contacts.remove(contact)
            print("Contact supprimé avec succès.")
        else:
            print("Contact introuvable.")

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
                    if len(valeurs) == 4:  # Vérifie que la ligne contient exactement 4 valeurs
                        nom, prenom, email, telephone = valeurs
                        self.contacts.append(Contact(nom, prenom, email, telephone))
                    else:
                        print(f"Ligne ignorée : {ligne.strip()} (format incorrect)")


    def exporter_contacts_txt(self):
        """Export contacts in a table format to a text file."""
        with open("export_contacts.txt", "w") as f:
            header = f"{'Nom':<20}{'Prénom':<20}{'Email':<30}{'Téléphone':<15}\n"
            f.write(header)
            f.write("-" * len(header) + "\n")
            for contact in self.contacts:
                ligne = f"{contact.nom:<20}{contact.prenom:<20}{contact.email:<30}{contact.telephone:<15}\n"
                f.write(ligne)
        print("Contacts exportés dans 'export_contacts.txt' avec succès.")

# 4. Interaction avec l'Utilisateur
class Main:
    def __init__(self):
        self.gestionnaire = GestionnaireContact()

    def menu(self):
        while True:
            print("\n--- Gestionnaire de Contacts ---")
            print("1. Ajouter un nouveau contact")
            print("2. Consulter la liste de tous les contacts")
            print("3. Rechercher un contact par nom")
            print("4. Modifier un contact existant")
            print("5. Supprimer un contact")
            print("6. Exporter les contacts au format texte")
            print("7. Quitter")
            choix = input("Choisissez une option : ")

            if choix == "1":
                self.ajouter_contact()
            elif choix == "2":
                self.gestionnaire.afficher_contacts()
            elif choix == "3":
                self.rechercher_contact()
            elif choix == "4":
                self.modifier_contact()
            elif choix == "5":
                self.supprimer_contact()
            elif choix == "6":
                self.gestionnaire.exporter_contacts_txt()
            elif choix == "7":
                self.gestionnaire.sauvegarder_contacts()
                print("Données sauvegardées. Au revoir !")
                break
            else:
                print("Option invalide, veuillez réessayer.")

    def ajouter_contact(self):
        print("\n--- Ajouter un Contact ---")
        nom = input("Nom : ")
        prenom = input("Prénom : ")
        email = input("Email : ")
        telephone = input("Téléphone : ")
        contact = Contact(nom, prenom, email, telephone)
        self.gestionnaire.ajouter_contact(contact)
        print("Contact ajouté avec succès !")

    def rechercher_contact(self):
        print("\n--- Rechercher un Contact ---")
        nom = input("Nom du contact à rechercher : ")
        contact = self.gestionnaire.rechercher_contact(nom)
        if contact:
            print("Contact trouvé :")
            print(contact)
        else:
            print("Aucun contact trouvé avec ce nom.")

    def modifier_contact(self):
        print("\n--- Modifier un Contact ---")
        nom = input("Nom du contact à modifier : ")
        self.gestionnaire.modifier_contact(nom)

    def supprimer_contact(self):
        print("\n--- Supprimer un Contact ---")
        nom = input("Nom du contact à supprimer : ")
        self.gestionnaire.supprimer_contact(nom)


if __name__ == "__main__":
    app = Main()
    app.menu()
