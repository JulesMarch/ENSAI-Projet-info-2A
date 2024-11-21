## Importation des packages

import tkinter as tk
from tkinter import font, messagebox, ttk
from PIL import Image, ImageTk
import os
from src.dao.zonage_dao import ZonageDao

# Authentification
class AuthWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Authentification")
        self.root.geometry("300x250")

        # Créer les labels et les champs d'entrée
        self.label_username = tk.Label(root, text="Nom d'utilisateur:")
        self.label_username.pack(pady=10)

        self.entry_username = tk.Entry(root)
        self.entry_username.pack(pady=5)

        self.label_password = tk.Label(root, text="Mot de passe:")
        self.label_password.pack(pady=10)

        self.entry_password = tk.Entry(root, show="*")  # Le mot de passe sera masqué
        self.entry_password.pack(pady=5)

        # Créer les boutons de connexion et d'inscription
        self.button_login = tk.Button(root, text="Se connecter", command=self.check_credentials)
        self.button_login.pack(pady=10)

        self.button_register = tk.Button(root, text="Créer un compte", command=self.open_register_window)
        self.button_register.pack(pady=5)

    def check_credentials(self):
        # Validation des informations d'identification
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Lire les comptes enregistrés
        if os.path.exists("users.txt"):
            with open("users.txt", "r") as file:
                users = dict(line.strip().split(",") for line in file)
            
            # Vérification du nom d'utilisateur et du mot de passe
            if username in users and users[username] == password:
                messagebox.showinfo("Succès", "Connexion réussie !")
                self.open_main_window()  # Ouvrir la fenêtre principale
            else:
                messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            messagebox.showerror("Erreur", "Aucun compte n'est enregistré.")

    def open_main_window(self):
        self.root.withdraw()  # Masquer la fenêtre d'authentification
        new_window = tk.Toplevel()  # Créer une nouvelle fenêtre
        MainWindow(new_window)  # Passer cette nouvelle fenêtre à MainWindow

    def open_register_window(self):
        self.root.withdraw()
        RegisterWindow(self)

# Fenêtre pour créer un nouveau compte
class RegisterWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel()
        self.window.title("Créer un compte")
        self.window.geometry("300x200")

        # Créer les labels et les champs d'entrée pour l'inscription
        self.label_username = tk.Label(self.window, text="Nom d'utilisateur:")
        self.label_username.pack(pady=10)

        self.entry_username = tk.Entry(self.window)
        self.entry_username.pack(pady=5)

        self.label_password = tk.Label(self.window, text="Mot de passe:")
        self.label_password.pack(pady=10)

        self.entry_password = tk.Entry(self.window, show="*")  # Le mot de passe sera masqué
        self.entry_password.pack(pady=5)

        # Créer le bouton d'inscription
        self.button_register = tk.Button(self.window, text="S'inscrire", command=self.register_user)
        self.button_register.pack(pady=20)

        # Créer un bouton pour revenir à la fenêtre de connexion
        self.button_back = tk.Button(self.window, text="Retour", command=self.back_to_login)
        self.button_back.pack(pady=5)

    def register_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Vérification si l'utilisateur existe déjà
        if os.path.exists("users.txt"):
            with open("users.txt", "r") as file:
                users = dict(line.strip().split(",") for line in file)
            if username in users:
                messagebox.showerror("Erreur", "Ce nom d'utilisateur existe déjà.")
                return

        # Ajouter l'utilisateur au fichier
        with open("users.txt", "a") as file:
            file.write(f"{username},{password}\n")
        messagebox.showinfo("Succès", "Compte créé avec succès !")
        self.back_to_login()

    def back_to_login(self):
        self.window.destroy()  # Fermer la fenêtre d'inscription
        self.parent.root.deiconify()  # Rendre la fenêtre de connexion visible

# Fenêtre principale (MainWindow)
class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Menu Principal")
        self.root.geometry("1000x600")

        # Charger l'image de fond
        self.background_image = Image.open("Interface/Zoom_Paris.jpg")
        self.background_image = self.background_image.resize((1000, 600))
        self.bg_image = ImageTk.PhotoImage(self.background_image)

        # Créer un label pour afficher l'image de fond
        background_label = tk.Label(self.root, image=self.bg_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Créer une police en gras
        bold_font = font.Font(family="Arial", size=48, weight="bold")
        bold_font_sub = font.Font(family="Arial", size=12, weight="bold")

        # Créer le titre et un message sur la page d'acceuil
        label = tk.Label(self.root, text=" Vous êtes ici !🎯", font=bold_font, relief="solid", bd="2", fg="white", bg="green", justify="center")
        texte_desc = "Bienvenue dans l'application ! Vous pouvez choisir la fonctionnalité que vous voulez afin d'en savoir plus sur le territoire Français"
        description = tk.Label(self.root, text=texte_desc, font=bold_font_sub, wraplength=300, relief="solid", bd="2", justify="center", bg="light green")

        # Boutons pour ouvrir les autres fenêtres
        button_open_second = tk.Button(self.root, text="Connaître les localisations", font=bold_font_sub, command=self.open_second_window)
        button_open_third = tk.Button(self.root, text="Où est mon point ?", font=bold_font_sub, command=self.open_third_window)

        # Positionner les widgets
        label.place(x=250, y=50)
        description.place(x=350, y=150)
        button_open_second.place(x=385, y=300, width=230, height=70)
        button_open_third.place(x=385, y=400, width=230, height=70)

    def open_second_window(self):
        self.root.withdraw()
        SecondWindow(self)

    def open_third_window(self):
        self.root.withdraw()
        ThirdWindow(self)

# Fenêtre secondaire
class SecondWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel()
        self.window.title("Fonction information")
        self.window.geometry("600x600")

        # Charger l'image de fond
        self.background_image = Image.open("Interface/Fonction 1.jpg")
        self.background_image = self.background_image.resize((600, 600))
        self.bg_image = ImageTk.PhotoImage(self.background_image)

        # Créer un label pour afficher l'image de fond
        background_label = tk.Label(self.window, image=self.bg_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Créer une police pour uniformiser la fenêtre
        bold_font = font.Font(family="Arial", size=48, weight="bold")
        bold_font_sub = font.Font(family="Arial", size=12, weight="bold")

        # Créer un titre
        label = tk.Label(self.window, text="Fonction 1", relief="solid", bd="2", font=bold_font, bg="orange")
        label.place(x=130, y=50)

        # Insérer un texte contenant des instructions 
        texte = "Indiquez le zonage dont vous souhaitez connaître plus d'informations puis cliquez sur le bouton Valider"
        instruction = tk.Label(self.window, text=texte, font=bold_font_sub, wraplength=300, relief="solid", bd="2", justify="center", bg="orange")
        instruction.place(x=175, y=200)
        
        # Zone de texte 1
        self.text_entry_1 = tk.Entry(self.window, width=30)
        self.text_entry_1.place(x=200, y=300, width=200, height=30)

        # Menu déroulant
        self.options = ["Région", "Département", "Commune", "Arrondissement", "IRIS"]
        self.combo_box = ttk.Combobox(self.window, values=self.options, state="readonly")
        self.combo_box.place(x=200, y=350, width=200, height=30)
        self.combo_box.current(0)  # Sélectionner la première option par défaut

        # Bouton de validation pour récupérer le texte
        button_valider = tk.Button(self.window, text="Valider", font=bold_font_sub, command=self.valider_texte)
        button_valider.place(x=260, y=400, width=100, height=30)

        # Label pour afficher le résultat de la validation
        self.label_resultat = tk.Label(self.window, text="", font=bold_font_sub, bg="white")
        self.label_resultat.place(x=185, y=450)

        button_back_main = tk.Button(self.window, text="Retour au menu principal", font=bold_font_sub, command=self.return_to_main_window)
        button_back_main.place(x=200, y=500, width=200, height=50)

        self.window.protocol("WM_DELETE_WINDOW", self.return_to_main_window)

    def valider_texte(self):
        # Récupérer les textes des deux zones de texte et les afficher dans le label
        texte_1 = self.text_entry_1.get()
        option_selectionnee = self.combo_box.get()
        self.label_resultat.config(text=f"{ZonageDao.find_by_code_insee(texte_1, option_selectionnee)}")

    def return_to_main_window(self):
        self.window.destroy()
        self.parent.root.deiconify()

# Fenêtre tertiaire
class ThirdWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel()
        self.window.title("Fenêtre Tertiaire")
        self.window.geometry("600x600")

        # Charger l'image de fond
        self.background_image = Image.open("Interface/Fonction 2.jpg")
        self.background_image = self.background_image.resize((600, 600))
        self.bg_image = ImageTk.PhotoImage(self.background_image)

        # Créer un label pour afficher l'image de fond
        background_label = tk.Label(self.window, image=self.bg_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Créer une police en gras
        bold_font = font.Font(family="Arial", size=48, weight="bold")
        bold_font_sub = font.Font(family="Arial", size=12, weight="bold")

        # Créer un titre avec du texte en gras
        label = tk.Label(self.window, text="Fonction 2", font=bold_font, bg="white")
        label.place(x=150, y=50)
        
        button_back_main = tk.Button(self.window, text="Retour au menu principal", font=bold_font_sub, command=self.return_to_main_window)
        button_back_main.place(x=240, y=150, width=160, height=70)

        self.window.protocol("WM_DELETE_WINDOW", self.return_to_main_window)

    def return_to_main_window(self):
        self.window.destroy()
        self.parent.root.deiconify()

# Application principale
if __name__ == "__main__":
    root = tk.Tk()
    app = AuthWindow(root)
    root.mainloop()