import sqlite3
import customtkinter as ctk
from PIL import Image
import pywinstyles
import hashlib
from tkinter import filedialog
from tkinter import ttk

class AresSystem:
    def __init__(self):
        self.connessione = sqlite3.connect('Ares.db')
        self.cursore = self.connessione.cursor()
        self.create_db()

    def create_db(self):
        self.cursore.execute('''
        CREATE TABLE IF NOT EXISTS utenti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome TEXT,
            Cognome TEXT,
            Password TEXT,
            Privilegio TEXT,
            Email TEXT,
            Cellulare INTEGER,
            N°Tessera INTEGER,
            Foto BLOB
        )
        ''')
        self.connessione.commit()
        
    def Check_Login_User_To_Add(self,Nome,Cognome):
        if Cognome.isalpha() and Nome.isalpha():
            return True
        else:
            print("Nome e cognome possono contenere solo lettere!")
            return False
    
    def Check_Login_User(self,Nome_Completo):
        parts = Nome_Completo.strip().split()
        if len(parts) != 2 or not all(p.isalpha() for p in parts):
            print("Nome e cognome possono contenere solo lettere!")
            return False
        self.cursore.execute("SELECT * FROM utenti WHERE (Nome||' '||Cognome)=?",(Nome_Completo,))
        esito=self.cursore.fetchone()
        if esito:
            print("Utente presente nel Database")
            return True
        else:
            print("Utente non presente nel Database")
            return False
        
    def search_user_del(self, Nome, Cognome):
        if not Nome.isalpha() or not Cognome.isalpha():
            return []
        self.cursore.execute("SELECT id, Nome, Cognome,Email,Cellulare,N°Tessera, Privilegio,Foto FROM utenti WHERE Nome=? AND Cognome=?",(Nome, Cognome))
        return self.cursore.fetchall()
    
    def get_user_by_id(self, id):
        self.cursore.execute("SELECT id, Nome, Cognome, Password, Email,Cellulare,N°Tessera, Privilegio,Foto FROM utenti WHERE id=?", (id,))
        return self.cursore.fetchone()
    
    def get_user_by_name(self,Nome_Completo):
        self.cursore.execute("SELECT id, Nome, Cognome, Password, Email,Cellulare,N°Tessera, Privilegio,Foto FROM utenti WHERE (Nome||' '||Cognome)=?", (Nome_Completo,))
        return self.cursore.fetchone()
    
    def search_user_del_Tessera(self,Tessera):
        if not Tessera.isdigit():
            return []
        self.cursore.execute("SELECT id, Nome, Cognome, Password,Email,Cellulare,N°Tessera, Privilegio,Foto FROM utenti WHERE N°Tessera=?",(Tessera,))
        return self.cursore.fetchall()
    
    def verify_password(self,Nome_Completo,Password_Inserita):
        Password_Hash = hashlib.sha256(Password_Inserita.encode()).hexdigest()
        self.cursore.execute("SELECT * FROM utenti WHERE (Nome||' '||Cognome)=? AND Password=?",(Nome_Completo,Password_Hash))
        esito=self.cursore.fetchone()
        if esito:
            print("Password corretta!!")
            return True
        else:
            print("Password Errata!!")
            return False
        
    def Add_User_Menu(self,Nome_cercato,Cognome_cercato, Password_Inserita,Privilegio_Inserito,Email_Inserita,Cellulare_Inserito,Tessera_Inserita,Foto_Inserita):
        if not Nome_cercato.isalpha() or not Cognome_cercato.isalpha():
            print("Nome e cognome possono contenere solo lettere!")
            return False
        Password_Hash = hashlib.sha256(Password_Inserita.encode()).hexdigest()
        query="INSERT INTO utenti (Nome,Cognome, Password, Privilegio,Email,Cellulare,N°Tessera,Foto) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        self.cursore.execute(query,(Nome_cercato,Cognome_cercato,Password_Hash,Privilegio_Inserito,Email_Inserita,Cellulare_Inserito,Tessera_Inserita,Foto_Inserita))
        print("Utente aggiunto con successo!")
        
        self.connessione.commit()
        return True
    
    def Update_User_Data_And_PSW(self,Id,Nome_cercato,Cognome_cercato, Password_Inserita,Privilegio_Inserito,Email_Inserita,Cellulare_Inserito,Tessera_Inserita,Foto_Inserita):
        if not Nome_cercato.isalpha() or not Cognome_cercato.isalpha():
            print("Nome e cognome possono contenere solo lettere!")
            return False
        Password_Hash = hashlib.sha256(Password_Inserita.encode()).hexdigest()
        query="UPDATE utenti SET Nome=?, Cognome=?, Password=?, Privilegio=?, Email=?, Cellulare=?, N°Tessera=?, Foto=? WHERE Id=?"
        self.cursore.execute(query,(Nome_cercato,Cognome_cercato,Password_Hash,Privilegio_Inserito,Email_Inserita,Cellulare_Inserito,Tessera_Inserita,Foto_Inserita,Id))
        print("Utente aggiornato con successo!")
        self.connessione.commit()
        
    def Update_User_Data_NO_PSW(self,Id,Nome_cercato,Cognome_cercato,Privilegio_Inserito,Email_Inserita,Cellulare_Inserito,Tessera_Inserita,Foto_Inserita):
        if not Nome_cercato.isalpha() or not Cognome_cercato.isalpha():
            print("Nome e cognome possono contenere solo lettere!")
            return False
        query="UPDATE utenti SET Nome=?, Cognome=?, Privilegio=?, Email=?, Cellulare=?, N°Tessera=?, Foto=? WHERE Id=?"
        self.cursore.execute(query,(Nome_cercato,Cognome_cercato,Privilegio_Inserito,Email_Inserita,Cellulare_Inserito,Tessera_Inserita,Foto_Inserita,Id))
        self.connessione.commit()
        
    def Update_Personal_Data_And_PSW(self,Nome_cercato,Cognome_cercato, Password_Inserita,Privilegio_Inserito,Email_Inserita,Cellulare_Inserito,Tessera_Inserita,Foto_Inserita,Nome_Completo):
        if not Nome_cercato.isalpha() or not Cognome_cercato.isalpha():
            print("Nome e cognome possono contenere solo lettere!")
            return False
        Password_Hash = hashlib.sha256(Password_Inserita.encode()).hexdigest()
        query="UPDATE utenti SET Nome=?, Cognome=?, Password=?, Privilegio=?, Email=?, Cellulare=?, N°Tessera=?, Foto=? WHERE (Nome || ' ' || Cognome) = ?"
        self.cursore.execute(query,(Nome_cercato,Cognome_cercato,Password_Hash,Privilegio_Inserito,Email_Inserita,Cellulare_Inserito,Tessera_Inserita,Foto_Inserita,Nome_Completo))
        print("Utente aggiornato con successo!")
        
        self.connessione.commit()
        
    def Update_Personal_Data_NO_PSW(self,Nome, Cognome, Privilegio, Email, Cellulare, Tessera, Foto,Utente):
        if not Nome.isalpha() or not Cognome.isalpha():
            print("Nome e cognome possono contenere solo lettere!")
            return False
        query = "UPDATE utenti SET Nome=?, Cognome=?, Privilegio=?, Email=?, Cellulare=?, N°Tessera=?, Foto=? WHERE (Nome || ' ' || Cognome) = ?"
        self.cursore.execute(query, (Nome, Cognome, Privilegio, Email, Cellulare, Tessera, Foto,Utente))
        self.connessione.commit()
        
    def Select_User(self,Nome_Completo):
        self.cursore.execute("SELECT * FROM utenti WHERE (Nome || ' ' || Cognome) = ? ",(Nome_Completo,))
        esito=self.cursore.fetchone()
        return esito
    
    def Select_privi(self,Nome_Completo):
        self.cursore.execute("SELECT Privilegio FROM utenti WHERE (Nome || ' ' || Cognome) = ? ",(Nome_Completo,))
        esito=self.cursore.fetchone()
        if esito is None:
            return None
        return esito[0]
        
    def delete_user(self,ID_conferma):
        self.cursore.execute("DELETE FROM utenti WHERE ID = ?", (ID_conferma,))
        self.connessione.commit()
        return True
    
    def Reset_Password(self,Nome,Cognome,Tessera,Password):
        if not Nome.isalpha() or not Cognome.isalpha():
            print("Nome e cognome possono contenere solo lettere!")
            return False
        Password_Hash = hashlib.sha256(Password.encode()).hexdigest()
        query="UPDATE utenti SET Password=? WHERE Nome=? AND Cognome=? AND N°Tessera=?"
        self.cursore.execute(query,(Password_Hash,Nome,Cognome,Tessera))
        self.connessione.commit()
        return True
            
    def show_database(self):
        self.cursore.execute("SELECT ID, Nome, Cognome,Email,Cellulare,N°Tessera,Privilegio,Foto FROM utenti")
        return self.cursore.fetchall()
        
    def salva_foto(self, nome_completo, percorso_foto):
        with open(percorso_foto, 'rb') as f:
            foto_bytes = f.read()
        self.cursore.execute("UPDATE utenti SET foto=? WHERE (Nome||' '||Cognome)=?",(foto_bytes, nome_completo))
        self.connessione.commit()

    def get_foto(self, nome_completo):
        self.cursore.execute("SELECT foto FROM utenti WHERE (Nome||' '||Cognome)=?",(nome_completo,))
        risultato = self.cursore.fetchone()
        return risultato[0] if risultato else None 

class AresGUI:
    def __init__(self):
        self.sistema = AresSystem()
        self.login_window = ctk.CTk(fg_color="BLACK")
        
        #===========SETTING WINDOW===================================================================
        self.login_window.title("ARES")
        self.login_window.geometry("1414x752")
        
        #===========SETTING IMAGE====================================================================
        img_data = Image.open("sfondo.png")
        img_leggera = img_data.resize((1414, 752), resample=Image.Resampling.NEAREST)
        self.bg_image = ctk.CTkImage(light_image=img_leggera, dark_image=img_leggera, size=(1414, 752))
        
        self.Show_Login_Window()
        
        self.login_window.mainloop()
        
        #================================SETTING ACCESS WINDOW=========================================
    def Show_Login_Window(self):
        self.Tentativi_rimasti=3
        
        self.frame_login=ctk.CTkFrame(self.login_window)
        self.frame_login.place(relx=0.5, rely=0.5, anchor="center",relheight=1,relwidth=1)
        
        self.bg_label_login = ctk.CTkLabel(self.frame_login, image=self.bg_image, text="")
        self.bg_label_login.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.login_window.bind("<Configure>", self.resize_background)
        
        #=============================GRAPHIC ELEMENT===================================================
        self.label_notifications = ctk.CTkLabel(self.frame_login, text="", font=("Arial", 20),bg_color="#000001")
        self.label_notifications.place(relx=0.5, rely=0.10, anchor="center")
        pywinstyles.set_opacity(self.label_notifications, color="#000001")
        
        self.TITLE = ctk.CTkLabel(self.frame_login, text="ACCESSO SISTEMA ARES",font=("Arial",70),bg_color="#000001")
        self.TITLE.place(relx=0.5, rely=0.25, anchor="center")       
        pywinstyles.set_opacity(self.TITLE, color="#000001")
        
        self.entry_name_login = ctk.CTkEntry(self.frame_login, placeholder_text="Nome e Cognome",font=("Arial",40),bg_color="#000001")
        self.entry_name_login.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.4)        
        pywinstyles.set_opacity(self.entry_name_login, color="#000001")
        
        self.label_PSW_FORG = ctk.CTkLabel(self.login_window, text="Hai dimenticato la password?", font=("Arial", 16, "underline"),text_color="WHITE",cursor="hand2",bg_color="#000001")
        self.label_PSW_FORG.bind("<Button-1>",self.Window_PSW_FRG)
        self.label_PSW_FORG.place(relx=0.5, rely=0.67, anchor="center")
        pywinstyles.set_opacity(self.label_PSW_FORG, color="#000001")
        
        self.button_access = ctk.CTkButton(self.frame_login, text="ACCEDI", command=self.Login,font=("Arial",40),bg_color="#000001")
        self.button_access.place(relx=0.5, rely=0.75, anchor="center", relwidth=0.2) 
        pywinstyles.set_opacity(self.button_access, color="#000001")
        
        self.Show_Hide_PSW_label= ctk.CTkLabel(self.frame_login, text="Mostra password", font=("Arial", 16, "underline"),text_color="WHITE",cursor="hand2",bg_color="#000001")
        self.Show_Hide_PSW_label.bind("<Button-1>",self.Show_Hide_PSW)
        self.Show_Hide_PSW_label.place(relx=0.75, rely=0.60, anchor="center",relwidth=0.2)
        pywinstyles.set_opacity(self.Show_Hide_PSW_label, color="#000001")
        
        self.entry_password = ctk.CTkEntry(self.frame_login, placeholder_text="Password",show="*",font=("Arial",40),bg_color="#000001")
        self.entry_password.place(relx=0.5, rely=0.60, anchor="center", relwidth=0.4)
        pywinstyles.set_opacity(self.entry_password, color="#000001")
        
        #==========================ACCESS WINDOW FUNCTION=====================================
    def Show_Hide_PSW(self,event=None):
        if self.entry_password.cget("show")=="*":
            self.entry_password.configure(show="")
            self.Show_Hide_PSW_label.configure(text="Nascondi password")
        else:
            self.entry_password.configure(show="*")
            self.Show_Hide_PSW_label.configure(text="Mostra password")
            
    def resize_background(self, event=None):
        if hasattr(self, "_after_id") and self._after_id:
            self.login_window.after_cancel(self._after_id)
        
        self._after_id = self.login_window.after(40, self._perform_effective_resizing)

    def _perform_effective_resizing(self):
        if not hasattr(self, "login_window") or self.login_window is None:
            return
            
        if not self.login_window.winfo_exists():
            return
            
        try:
            finestra_larga = self.login_window.winfo_width()
            finestra_alta = self.login_window.winfo_height()
            if finestra_larga > 10 and finestra_alta > 10:
                if hasattr(self, "bg_image") and self.bg_image is not None:
                    self.bg_image.configure(size=(finestra_larga, finestra_alta))
            
            self._after_id = None
            
        except Exception:
            return
            
    def Login(self):
        if self.Tentativi_rimasti<=0:
            self.label_notifications.configure(text="ACCESSO BLOCCATO TENTATIVI ESAURITI")
            self.entry_name_login.configure(state="disabled")
            self.entry_password.configure(state="disabled")
            self.button_access.configure(state="disabled")
            return
        
        nome_inserito = self.entry_name_login.get()
        password_inserita=self.entry_password.get()
        self.Nome_Loggato=nome_inserito
        
        if self.sistema.Check_Login_User(nome_inserito):
            self.Privilegio_Loggato = self.sistema.Select_privi(nome_inserito)
            if self.sistema.verify_password(nome_inserito,password_inserita):
                self.login_window.unbind("<Configure>")
                self.frame_login.destroy()
                self.MAIN_MENU()
            else:
                self.Tentativi_rimasti -=1
                self.label_notifications.configure(text=f"PASSWORD ERRATA {self.Tentativi_rimasti} TENTATIVI RIMASTI")
                self.entry_password.delete(0, "end")
                    
                if self.Tentativi_rimasti == 0:
                    self.label_notifications.configure(text="TENTATIVI ESAURITI!!")
                    self.entry_name_login.configure(state="disabled")
                    self.entry_password.configure(state="disabled")
                    self.button_access.configure(state="disabled")
        else:
            self.label_notifications.configure(text="UTENTE NON REGISTRATO!!")     
            
    #===========================MENU FUNCTION================================
    def Back_To_Main_Menu(self):
        sottomenu_attivi = ['HR_FRAME', 'Work_Frame']
        for menu in sottomenu_attivi:
            if hasattr(self, menu):
                widget = getattr(self, menu)
                if widget:
                    widget.destroy()
        
        self.MAIN_MENU()
        
    def Logout(self):
        if hasattr(self, 'frame_MENU') and self.frame_MENU:
            self.frame_MENU.destroy()
            
        sottomenu_attivi = ['HR_FRAME', 'Work_Frame']
        for menu in sottomenu_attivi:
            if hasattr(self, menu):
                widget = getattr(self, menu)
                if widget:
                    widget.destroy()
        
        self.Show_Login_Window()
        
    def Carica_Foto(self,label_target):
        percorso = filedialog.askopenfilename(filetypes=[("Immagini", "*.png *.jpg *.jpeg")])
        if percorso:
            self.foto_percorso = percorso
            img = Image.open(percorso)
            foto = ctk.CTkImage(img, size=(200, 250))
            label_target.configure(image=foto, text="")
            label_target.image = foto
            
    def Clear_Entry_Window(self):
        for widget in self.Window_User_frame_login.winfo_children():
            if isinstance(widget, ctk.CTkEntry):
                widget.delete(0, "end")
        self.Priv_Value.set("User")
        self.foto_percorso = None
        self.Label_photo_Show.configure(image="", text="Nessuna foto")
        
    def Clear_Entry(self):
        for widget in self.Work_Frame.winfo_children():
            if isinstance(widget, ctk.CTkEntry):
                widget.delete(0, "end")
        self.Priv_Value.set("User")
        self.foto_percorso = None
        self.Label_photo.configure(image="", text="Nessuna foto")
        
        #====================================SETTING MAIN MENU WIDGET===============================================
    def MAIN_MENU(self):
        if hasattr(self, 'HR_FRAME') and self.HR_FRAME:
            self.HR_FRAME.destroy()
            
        self.Work_Frame=ctk.CTkFrame(self.login_window,fg_color="#1E2229")
        self.Work_Frame.place(relx=1, rely=0.0, anchor="ne",relheight=1,relwidth=0.797)
        
        self.frame_MENU=ctk.CTkFrame(self.login_window,fg_color="#1E2229")
        self.frame_MENU.place(relx=0.0, rely=0.0, anchor="nw",relheight=1,relwidth=0.2)
        
        self.button1 = ctk.CTkButton(self.frame_MENU, text="👥 GESTIONE UTENTI", command=self.HR_MENU,font=("Arial black",20),text_color="WHITE",fg_color="#1E2229")
        self.button1.place(relx=0.0, rely=0.25, anchor="w", relwidth=1,relheight=0.5)
        pywinstyles.set_opacity(self.button1,value=0.5, color="#1E2229")
        
        self.button3 = ctk.CTkButton(self.frame_MENU, text="🚪 ESCI", command=self.Logout,font=("Arial black",20),text_color="WHITE",fg_color="#1E2229")
        self.button3.place(relx=0.0, rely=0.75, anchor="w", relwidth=1,relheight=0.5)
        pywinstyles.set_opacity(self.button3,value=0.5, color="#1E2229")

        
    #====================================SETTING HR MENU================================================================
    def HR_MENU(self):
        if hasattr(self, 'frame_MENU') and self.frame_MENU:
            self.frame_MENU.destroy()
            
        self.HR_FRAME=ctk.CTkFrame(self.login_window,fg_color="#1E2229")
        self.HR_FRAME.place(relx=0.0, rely=0.0, anchor="nw",relheight=1,relwidth=0.2)
        
        self.button1 = ctk.CTkButton(self.HR_FRAME, text="📋 LISTA UTENTI", command=self.Show_DB_Menu,font=("Arial black",20),text_color="WHITE",anchor="w",fg_color="#1E2229")
        self.button1.place(relx=0.0, rely=0.07, anchor="w", relwidth=1,relheight=0.142)
        pywinstyles.set_opacity(self.button1,value=0.5, color="#1E2229")
        
        self.button2 = ctk.CTkButton(self.HR_FRAME, text="🔍 RICERCA UTENTI", command=self.Search_User_Menu,font=("Arial black",20),text_color="WHITE",anchor="w",fg_color="#1E2229")
        self.button2.place(relx=0.0, rely=0.212, anchor="w", relwidth=1,relheight=0.142)
        pywinstyles.set_opacity(self.button2,value=0.5, color="#1E2229")

        self.button4 = ctk.CTkButton(self.HR_FRAME, text="🔐 MODIFICA SCHEDA\n PERSONALE", command=self.Modify_personal_Data,font=("Arial black",20),text_color="WHITE",anchor="w",fg_color="#1E2229")
        self.button4.place(relx=0.0, rely=0.354, anchor="w", relwidth=1,relheight=0.142)
        pywinstyles.set_opacity(self.button4,value=0.5, color="#1E2229")
        
        self.button5 = ctk.CTkButton(self.HR_FRAME, text="➕ AGGIUNGI UTENTE", command=self.Add_User_Menu,font=("Arial black",20),text_color="WHITE",anchor="w",fg_color="#1E2229")
        self.button5.place(relx=0.0, rely=0.496, anchor="w", relwidth=1,relheight=0.142)
        pywinstyles.set_opacity(self.button5,value=0.5, color="#1E2229")
        
        self.button6 = ctk.CTkButton(self.HR_FRAME, text="⚙️MODIFICA DATI UTENTE", command=self.Modify_User_Data,font=("Arial black",19),text_color="WHITE",anchor="w",fg_color="#1E2229")
        self.button6.place(relx=0.0, rely=0.638, anchor="w", relwidth=1,relheight=0.142)
        pywinstyles.set_opacity(self.button6,value=0.5, color="#1E2229")
        
        self.button7 = ctk.CTkButton(self.HR_FRAME, text="🗑️ELIMINA UTENTE", command=self.Delete_User_Menu,font=("Arial black",20),text_color="WHITE",anchor="w",fg_color="#1E2229")
        self.button7.place(relx=0.0, rely=0.78, anchor="w", relwidth=1,relheight=0.142)
        pywinstyles.set_opacity(self.button7,value=0.5, color="#1E2229")
        
        self.button8 = ctk.CTkButton(self.HR_FRAME, text="◀ INDIETRO", command=self.Back_To_Main_Menu,font=("Arial black",20),text_color="WHITE",anchor="w",fg_color="#1E2229")
        self.button8.place(relx=0.0, rely=0.922, anchor="w", relwidth=1,relheight=0.142)
        pywinstyles.set_opacity(self.button8,value=0.5, color="#1E2229")
        
        #===============================ALL HR MENU WIDGET AND FUNCTION=======================================================
    def Add_User_Menu(self):
        for widget in self.Work_Frame.winfo_children():
            widget.destroy()
        if self.Privilegio_Loggato=="Admin":
            for widget in self.Work_Frame.winfo_children():
                widget.destroy()
            #==============================ALL WIDGET=================================
            self.Title_Add = ctk.CTkLabel(self.Work_Frame, text="INSERISCI DATI DELL'UTENTE DA AGGIUNGERE", font=("Arial", 40),bg_color="#000001")
            self.Title_Add.place(relx=0.5, rely=0.06, anchor="center")
            pywinstyles.set_opacity(self.Title_Add, color="#000001")
            
            self.Label_name_add = ctk.CTkLabel(self.Work_Frame, text="NOME:", font=("Arial", 20),bg_color="#000001", anchor="e")
            self.Label_name_add.place(relx=0.02, rely=0.20, anchor="w")
            pywinstyles.set_opacity(self.Label_name_add, color="#000001")
            
            self.entry_name_add = ctk.CTkEntry(self.Work_Frame, placeholder_text="Nome",font=("Arial",20),bg_color="#000001")
            self.entry_name_add.place(relx=0.15, rely=0.20, anchor="w", relwidth=0.30)
            pywinstyles.set_opacity(self.entry_name_add, color="#000001")
            
            self.Label_Last_name_add = ctk.CTkLabel(self.Work_Frame, text="COGNOME:", font=("Arial", 20),bg_color="#000001", anchor="e")
            self.Label_Last_name_add.place(relx=0.02, rely=0.35, anchor="w")
            pywinstyles.set_opacity(self.Label_Last_name_add, color="#000001")
            
            self.entry_Last_name_add = ctk.CTkEntry(self.Work_Frame, placeholder_text="Cognome",font=("Arial",20),bg_color="#000001")
            self.entry_Last_name_add.place(relx=0.15, rely=0.35, anchor="w", relwidth=0.30)
            pywinstyles.set_opacity(self.entry_Last_name_add, color="#000001")
            
            self.Label_PSW_add = ctk.CTkLabel(self.Work_Frame, text="PASSWORD:", font=("Arial", 20),bg_color="#000001", anchor="e")
            self.Label_PSW_add.place(relx=0.02, rely=0.50,anchor="w")
            pywinstyles.set_opacity(self.Label_PSW_add, color="#000001")
            
            self.entry_PSW_add = ctk.CTkEntry(self.Work_Frame, placeholder_text="Password",font=("Arial",20),bg_color="#000001")
            self.entry_PSW_add.place(relx=0.15, rely=0.50, anchor="w", relwidth=0.30)
            pywinstyles.set_opacity(self.entry_PSW_add, color="#000001")
            
            self.Label_EMAIL_add = ctk.CTkLabel(self.Work_Frame, text="EMAIL:", font=("Arial", 20),bg_color="#000001", anchor="e")
            self.Label_EMAIL_add.place(relx=0.02, rely=0.65,anchor="w")
            pywinstyles.set_opacity(self.Label_EMAIL_add, color="#000001")
            
            self.entry_EMAIL_add = ctk.CTkEntry(self.Work_Frame, placeholder_text="Email",font=("Arial",20),bg_color="#000001")
            self.entry_EMAIL_add.place(relx=0.15, rely=0.65, anchor="w", relwidth=0.30)
            pywinstyles.set_opacity(self.entry_EMAIL_add, color="#000001")
            
            self.Label_CELL_add = ctk.CTkLabel(self.Work_Frame, text="CELLULARE:", font=("Arial", 20),bg_color="#000001", anchor="e")
            self.Label_CELL_add.place(relx=0.02, rely=0.80,anchor="w")
            pywinstyles.set_opacity(self.Label_CELL_add, color="#000001")
            
            self.entry_CELL_add = ctk.CTkEntry(self.Work_Frame, placeholder_text="Cellulare",font=("Arial",20),bg_color="#000001")
            self.entry_CELL_add.place(relx=0.15, rely=0.80, anchor="w", relwidth=0.30)
            pywinstyles.set_opacity(self.entry_CELL_add, color="#000001")
            
            self.Label_CARD_add = ctk.CTkLabel(self.Work_Frame, text="N°TESSERA:", font=("Arial", 20),bg_color="#000001", anchor="e")
            self.Label_CARD_add.place(relx=0.50, rely=0.80,anchor="w")
            pywinstyles.set_opacity(self.Label_CARD_add, color="#000001")
            
            self.entry_CARD_add = ctk.CTkEntry(self.Work_Frame, placeholder_text="N°Tessera",font=("Arial",20),bg_color="#000001")
            self.entry_CARD_add.place(relx=0.63, rely=0.80, anchor="w", relwidth=0.30)
            pywinstyles.set_opacity(self.entry_CARD_add, color="#000001")
            
            self.Label_PRIV_add = ctk.CTkLabel(self.Work_Frame, text="PRIVILEGIO:", font=("Arial", 20),bg_color="#000001", anchor="e")
            self.Label_PRIV_add.place(relx=0.50, rely=0.65,anchor="w")
            pywinstyles.set_opacity(self.Label_PRIV_add, color="#000001")
            
            self.Priv_Value = ctk.StringVar(value="")
            self.Priv_button_1 = ctk.CTkRadioButton(self.Work_Frame, text="Admin", variable= self.Priv_Value, value="Admin")
            self.Priv_button_1.place(relx=0.65, rely=0.65, anchor="w", relwidth=0.30)
            self.Priv_button_2 = ctk.CTkRadioButton(self.Work_Frame, text="User", variable= self.Priv_Value, value="User")
            self.Priv_button_2.place(relx=0.80, rely=0.65, anchor="w", relwidth=0.30)
            
            self.button_SAVE = ctk.CTkButton(self.Work_Frame, text="SALVA", command=self.Add_User_Menu_Fun,font=("Arial black",20),text_color="WHITE",fg_color="#1E2229")
            self.button_SAVE.place(relx=0.75, rely=0.935, anchor="center", relwidth=0.50,relheight=0.125)
            pywinstyles.set_opacity(self.button_SAVE,value=0.5, color="#1E2229")
             
            self.button_CLEAR = ctk.CTkButton(self.Work_Frame, text="RESET", command=self.Clear_Entry,font=("Arial black",20),text_color="WHITE",fg_color="#1E2229")
            self.button_CLEAR.place(relx=0.25, rely=0.935, anchor="center", relwidth=0.50,relheight=0.125)
            pywinstyles.set_opacity(self.button_CLEAR,value=0.5, color="#1E2229")
            
            self.label_Error = ctk.CTkLabel(self.Work_Frame, text="", font=("Arial", 20),bg_color="#000001")
            self.label_Error.place(relx=0.5, rely=0.13, anchor="center")
            pywinstyles.set_opacity(self.label_Error, color="#000001")
            #=======================SETTING PHOTO======================
            self.foto_percorso = None
        
            self.Label_FOTO_add = ctk.CTkLabel(self.Work_Frame, text="FOTO:", font=("Arial", 20), bg_color="#000001", anchor="e")
            self.Label_FOTO_add.place(relx=0.50, rely=0.35, anchor="w")
            pywinstyles.set_opacity(self.Label_FOTO_add, color="#000001")
            
            self.button_FOTO = ctk.CTkButton(self.Work_Frame, text="📁 CARICA FOTO",command=lambda: self.Carica_Foto(self.Label_photo), font=("Arial", 20), fg_color="#1E2229", text_color="WHITE")
            self.button_FOTO.place(relx=0.60, rely=0.50, anchor="w", relwidth=0.30)
            pywinstyles.set_opacity(self.button_FOTO, value=0.5, color="#1E2229")
            
            self.Label_photo = ctk.CTkLabel(self.Work_Frame, text="Nessuna foto", fg_color="#1E2229", corner_radius=8)
            self.Label_photo.place(relx=0.75, rely=0.29, anchor="center", relwidth=0.30, relheight=0.50)
            pywinstyles.set_opacity(self.Label_photo, value=0.5, color="#1E2229")
        else:
            self.label_Error_Privi = ctk.CTkLabel(self.Work_Frame, text="🔒 ACCESSO NON AUTORIZZATO\n CONTATTA UN SUPERVISORE", font=("Arial", 40),text_color="RED")
            self.label_Error_Privi.place(relx=0.5, rely=0.5, anchor="center")
            pywinstyles.set_opacity(self.label_Error_Privi, color="#000001")
             
    def Add_User_Menu_Fun(self):
        Nome=self.entry_name_add.get()
        Cognome=self.entry_Last_name_add.get()
        Password=self.entry_PSW_add.get()
        Privilegio = self.Priv_Value.get()
        Email=self.entry_EMAIL_add.get()
        Cellulare=self.entry_CELL_add.get()
        Tessera=self.entry_CARD_add.get()
        Foto=self.foto_percorso
        
        campi_obbligatori = [self.entry_name_add, self.entry_Last_name_add, self.entry_PSW_add, self.entry_EMAIL_add, self.entry_CARD_add]
        tutti_compilati = all(widget.get().strip() != "" for widget in campi_obbligatori) and Privilegio != ""
        
        if not tutti_compilati:
            self.label_Error.configure(text="ATTENZIONE: DEVI INSERIRE TUTTI I DATI OBBLIGATORI", text_color="RED")
            return
        
        if self.sistema.Check_Login_User_To_Add(Nome,Cognome): 
            self.sistema.Add_User_Menu(Nome, Cognome, Password, Privilegio, Email, Cellulare, Tessera, Foto)
            self.label_Error.configure(text="UTENTE INSERITO CON SUCCESSO!", text_color="GREEN")
            self.Clear_Entry()
        else:
            self.label_Error.configure(text="NOME UTENTE NON VALIDO",text_color="RED")
    
    def Delete_User_Menu(self):
        for widget in self.Work_Frame.winfo_children():
            widget.destroy()
        if self.Privilegio_Loggato=="Admin":
            for widget in self.Work_Frame.winfo_children():
                widget.destroy()
            #==============================ALL WIDGET=================================
            self.Title_Add = ctk.CTkLabel(self.Work_Frame, text="INSERISCI DATI DELL'UTENTE DA ELIMINARE", font=("Arial", 40),fg_color="transparent")
            self.Title_Add.place(relx=0.5, rely=0.06, anchor="center")
            pywinstyles.set_opacity(self.Title_Add, color="#000001")
                
            self.Label_name_Del = ctk.CTkLabel(self.Work_Frame, text="NOME:", font=("Arial", 20),fg_color="transparent", anchor="e")
            self.Label_name_Del.place(relx=0.02, rely=0.13, anchor="w")
            pywinstyles.set_opacity(self.Label_name_Del, color="#000001")
                
            self.entry_name_Del = ctk.CTkEntry(self.Work_Frame, placeholder_text="Nome",font=("Arial",20),fg_color="transparent")
            self.entry_name_Del.place(relx=0.15, rely=0.13, anchor="w", relwidth=0.30)
            pywinstyles.set_opacity(self.entry_name_Del, color="#000001")
                
            self.Label_Last_name_Del = ctk.CTkLabel(self.Work_Frame, text="COGNOME:", font=("Arial", 20),fg_color="transparent", anchor="e")
            self.Label_Last_name_Del.place(relx=0.50, rely=0.13, anchor="w")
            pywinstyles.set_opacity(self.Label_Last_name_Del, color="#000001")
                
            self.entry_Last_name_Del = ctk.CTkEntry(self.Work_Frame, placeholder_text="Cognome",font=("Arial",20),fg_color="transparent")
            self.entry_Last_name_Del.place(relx=0.63, rely=0.13, anchor="w", relwidth=0.30)
            pywinstyles.set_opacity(self.entry_Last_name_Del, color="#000001")
            
            self.Label_info = ctk.CTkLabel(self.Work_Frame, text="PUOI INSERIRE ANCHE SOLO IL N° DI TESSERAMENTO", font=("Arial", 20),fg_color="transparent")
            self.Label_info.place(relx=0.47, rely=0.25, anchor="w")
            pywinstyles.set_opacity(self.Label_info, color="#000001")
            
            self.Label_Error = ctk.CTkLabel(self.Work_Frame, text="", font=("Arial", 20),bg_color="#000001")
            self.Label_Error.place(relx=0.5, rely=0.19, anchor="center")
            pywinstyles.set_opacity(self.Label_Error, color="#000001")
            
            self.Label_NTessera_Del = ctk.CTkLabel(self.Work_Frame, text="N°TESSERA:", font=("Arial", 20),fg_color="transparent", anchor="e")
            self.Label_NTessera_Del.place(relx=0.02, rely=0.25, anchor="w")
            pywinstyles.set_opacity(self.Label_NTessera_Del, color="#000001")
                
            self.entry_NTessera_Del = ctk.CTkEntry(self.Work_Frame, placeholder_text="N°Tessera",font=("Arial",20),fg_color="transparent")
            self.entry_NTessera_Del.place(relx=0.15, rely=0.25, anchor="w", relwidth=0.30)
            pywinstyles.set_opacity(self.entry_NTessera_Del, color="#000001")
            
            self.button_SEARCH = ctk.CTkButton(self.Work_Frame, text="🔍 CERCA", command=self.Search_User_For_Del, font=("Arial", 20), fg_color="#1E2229", text_color="WHITE")
            self.button_SEARCH.place(relx=0.30, rely=0.30, anchor="w", relwidth=0.30)
            pywinstyles.set_opacity(self.button_SEARCH, value=0.5, color="#1E2229")
        else:
            self.label_Error_Privi = ctk.CTkLabel(self.Work_Frame, text="🔒 ACCESSO NON AUTORIZZATO\n CONTATTA UN SUPERVISORE", font=("Arial", 40),text_color="RED")
            self.label_Error_Privi.place(relx=0.5, rely=0.5, anchor="center")
            pywinstyles.set_opacity(self.label_Error_Privi, color="#000001")
            
    def Search_User_For_Del (self):
        Nome_Cercato=self.entry_name_Del.get()
        Cognome_Cercato=self.entry_Last_name_Del.get()
        N_Tessera_cercata=self.entry_NTessera_Del.get()
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",background="#1E2229",foreground="white",fieldbackground="#1E2229",rowheight=30)
        style.configure("Treeview.Heading",background="#14171A",foreground="white")

        
        risultati = self.sistema.search_user_del(Nome_Cercato, Cognome_Cercato)
        risultato_tessera=self.sistema.search_user_del_Tessera(N_Tessera_cercata)
        
        if risultati or risultato_tessera:
            self.tree = ttk.Treeview(self.Work_Frame, columns=("ID", "Nome", "Cognome","Email","Cellulare","N° Tessera", "Privilegio", ), show="headings")
            self.tree.heading("ID", text="ID")
            self.tree.heading("Nome", text="Nome")
            self.tree.heading("Cognome", text="Cognome")
            self.tree.heading("Email", text="Email")
            self.tree.heading("Cellulare", text="Cellulare")
            self.tree.heading("N° Tessera", text="N° Tessera")
            self.tree.heading("Privilegio", text="Privilegio")
            self.tree.place(relx=0.5, rely=0.55, anchor="center", relwidth=0.9, relheight=0.4)
            if risultati:
                for riga in risultati:
                    self.Label_Error.configure(text="",bg_color="#000001")
                    self.tree.insert("", "end", values=riga)
            elif risultato_tessera:
                for riga in risultato_tessera:
                    self.Label_Error.configure(text="",bg_color="#000001")
                    self.tree.insert("", "end", values=riga)
                    
            self.Label_ID_Del = ctk.CTkLabel(self.Work_Frame, text="DIGITA ID DA RIMUOVERE:", font=("Arial", 20),fg_color="transparent", anchor="e")
            self.Label_ID_Del.place(relx=0.02, rely=0.80, anchor="w")
            pywinstyles.set_opacity(self.Label_ID_Del, color="#000001")
                
            self.entry_ID_Del = ctk.CTkEntry(self.Work_Frame, placeholder_text="Id",font=("Arial",20),fg_color="transparent")
            self.entry_ID_Del.place(relx=0.30, rely=0.80, anchor="w", relwidth=0.30)
            pywinstyles.set_opacity(self.entry_ID_Del, color="#000001")
            
            self.button_DEL = ctk.CTkButton(self.Work_Frame, text="🗑️ELIMINA UTENTE", command=self.Delete_User, font=("Arial", 20), fg_color="#1E2229", text_color="WHITE")
            self.button_DEL.place(relx=0.63, rely=0.80, anchor="w", relwidth=0.30)
            pywinstyles.set_opacity(self.button_DEL, value=0.5, color="#1E2229")
        else:
             self.Label_Error.configure(text="UTENTE NON PRESENTE NEL DATABASE", text_color="RED")  
             
    def Delete_User(self):
        for elemento in self.tree.get_children():
            self.tree.delete(elemento)
        
        id=self.entry_ID_Del.get()
        if self.sistema.delete_user(id):
            self.Label_ID_Del = ctk.CTkLabel(self.Work_Frame, text="UTENTE RIMOSSO", font=("Arial", 20),fg_color="transparent", anchor="e",text_color="GREEN")
            self.Label_ID_Del.place(relx=0.40, rely=0.90, anchor="w")
            pywinstyles.set_opacity(self.Label_ID_Del, color="#000001")
        else:
            self.Label_ID_Del = ctk.CTkLabel(self.Work_Frame, text="ELIMINAZIONE NON RIUSCITA", font=("Arial", 20),fg_color="transparent", anchor="e",text_color="RED")
            self.Label_ID_Del.place(relx=0.40, rely=0.90, anchor="w")
            pywinstyles.set_opacity(self.Label_ID_Del, color="#000001")
    
    def Show_DB_Menu(self):
        for widget in self.Work_Frame.winfo_children():
            widget.destroy()
        
        Vista_db=self.sistema.show_database()
        #============================================= WIDGET ================================================================
        self.Title_Add = ctk.CTkLabel(self.Work_Frame, text="LISTA UTENTI REGISTRATI", font=("Arial", 40),fg_color="transparent")
        self.Title_Add.place(relx=0.5, rely=0.06, anchor="center")
        pywinstyles.set_opacity(self.Title_Add, color="#000001")
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",background="#1E2229",foreground="white",fieldbackground="#1E2229",rowheight=30)
        style.configure("Treeview.Heading",background="#14171A",foreground="white")
        self.tree = ttk.Treeview(self.Work_Frame, columns=("ID", "Nome", "Cognome","Email","Cellulare","N° Tessera", "Privilegio","Foto" ), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Cognome", text="Cognome")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Cellulare", text="Cellulare")
        self.tree.column("Cellulare", width=80)
        self.tree.heading("N° Tessera", text="N° Tessera")
        self.tree.column("N° Tessera", width=80)
        self.tree.heading("Privilegio", text="Privilegio")
        self.tree.column("Privilegio", width=75)
        self.tree.heading("Foto", text="Foto")
        self.tree.place(relx=0.5, rely=0.55, anchor="center", relwidth=0.9, relheight=0.7)
        for riga in Vista_db:
            self.tree.insert("", "end", values=riga)
    
    def Modify_User_Data(self):
        for widget in self.Work_Frame.winfo_children():
            widget.destroy()
        if self.Privilegio_Loggato=="Admin":
            for widget in self.Work_Frame.winfo_children():
                widget.destroy()
                
            self.Title_Add = ctk.CTkLabel(self.Work_Frame, text="INSERISCI DATI DELL'UTENTE DA VISUALIZZARE", font=("Arial", 40),fg_color="transparent")
            self.Title_Add.place(relx=0.5, rely=0.06, anchor="center")
            pywinstyles.set_opacity(self.Title_Add, color="#000001")
                
            self.Label_name_Del = ctk.CTkLabel(self.Work_Frame, text="NOME:", font=("Arial", 20),fg_color="transparent", anchor="e")
            self.Label_name_Del.place(relx=0.02, rely=0.13, anchor="w")
            pywinstyles.set_opacity(self.Label_name_Del, color="#000001")
                
            self.entry_name_Del = ctk.CTkEntry(self.Work_Frame, placeholder_text="Nome",font=("Arial",20),fg_color="transparent")
            self.entry_name_Del.place(relx=0.15, rely=0.13, anchor="w", relwidth=0.30)
            pywinstyles.set_opacity(self.entry_name_Del, color="#000001")
                
            self.Label_Last_name_Del = ctk.CTkLabel(self.Work_Frame, text="COGNOME:", font=("Arial", 20),fg_color="transparent", anchor="e")
            self.Label_Last_name_Del.place(relx=0.50, rely=0.13, anchor="w")
            pywinstyles.set_opacity(self.Label_Last_name_Del, color="#000001")
                
            self.entry_Last_name_Del = ctk.CTkEntry(self.Work_Frame, placeholder_text="Cognome",font=("Arial",20),fg_color="transparent")
            self.entry_Last_name_Del.place(relx=0.63, rely=0.13, anchor="w", relwidth=0.30)
            pywinstyles.set_opacity(self.entry_Last_name_Del, color="#000001")
            
            self.Label_info = ctk.CTkLabel(self.Work_Frame, text="PUOI INSERIRE ANCHE SOLO IL N° DI TESSERAMENTO", font=("Arial", 20),fg_color="transparent")
            self.Label_info.place(relx=0.47, rely=0.25, anchor="w")
            pywinstyles.set_opacity(self.Label_info, color="#000001")
            
            self.Label_Error = ctk.CTkLabel(self.Work_Frame, text="", font=("Arial", 20),bg_color="#000001")
            self.Label_Error.place(relx=0.5, rely=0.19, anchor="center")
            pywinstyles.set_opacity(self.Label_Error, color="#000001")
            
            self.Label_NTessera_Del = ctk.CTkLabel(self.Work_Frame, text="N°TESSERA:", font=("Arial", 20),fg_color="transparent", anchor="e")
            self.Label_NTessera_Del.place(relx=0.02, rely=0.25, anchor="w")
            pywinstyles.set_opacity(self.Label_NTessera_Del, color="#000001")
                
            self.entry_NTessera_Del = ctk.CTkEntry(self.Work_Frame, placeholder_text="N°Tessera",font=("Arial",20),fg_color="transparent")
            self.entry_NTessera_Del.place(relx=0.15, rely=0.25, anchor="w", relwidth=0.30)
            pywinstyles.set_opacity(self.entry_NTessera_Del, color="#000001")
            
            self.button_SEARCH = ctk.CTkButton(self.Work_Frame, text="🔍 CERCA", command=self.Search_User_for_data, font=("Arial", 20), fg_color="#1E2229", text_color="WHITE")
            self.button_SEARCH.place(relx=0.30, rely=0.30, anchor="w", relwidth=0.30)
            pywinstyles.set_opacity(self.button_SEARCH, value=0.5, color="#1E2229")
        else:
             self.label_Error_Privi = ctk.CTkLabel(self.Work_Frame, text="🔒 ACCESSO NON AUTORIZZATO\n CONTATTA UN SUPERVISORE", font=("Arial", 40),text_color="RED")
             self.label_Error_Privi.place(relx=0.5, rely=0.5, anchor="center")
             pywinstyles.set_opacity(self.label_Error_Privi, color="#000001")
             
    def Search_User_for_data (self):
        Nome_Cercato=self.entry_name_Del.get()
        Cognome_Cercato=self.entry_Last_name_Del.get()
        N_Tessera_cercata=self.entry_NTessera_Del.get()
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",background="#1E2229",foreground="white",fieldbackground="#1E2229",rowheight=30)
        style.configure("Treeview.Heading",background="#14171A",foreground="white")

        
        risultati = self.sistema.search_user_del(Nome_Cercato, Cognome_Cercato)
        risultato_tessera=self.sistema.search_user_del_Tessera(N_Tessera_cercata)
        
        if risultati or risultato_tessera:
            self.Table = ttk.Treeview(self.Work_Frame, columns=("ID", "Nome", "Cognome","Password","Email","Cellulare","N° Tessera", "Privilegio","Foto" ), show="headings")
            self.Table.heading("ID", text="ID")
            self.Table.column("ID", width=80)
            self.Table.heading("Nome", text="Nome")
            self.Table.heading("Cognome", text="Cognome")
            self.Table.heading("Password", text="Password")
            self.Table.column("Password", width=80)
            self.Table.heading("Email", text="Email")
            self.Table.heading("Cellulare", text="Cellulare")
            self.Table.column("Cellulare", width=80)
            self.Table.heading("N° Tessera", text="N° Tessera")
            self.Table.column("N° Tessera", width=80)
            self.Table.heading("Privilegio", text="Privilegio")
            self.Table.column("Privilegio", width=75)
            self.Table.heading("Foto", text="Foto")
            self.Table.place(relx=0.5, rely=0.55, anchor="center", relwidth=0.95, relheight=0.4)
            if risultati:
                for riga in risultati:
                    self.Label_Error.configure(text="",bg_color="#000001")
                    self.Table.insert("", "end", values=riga)
            elif risultato_tessera:
                for riga in risultato_tessera:
                    self.Label_Error.configure(text="",bg_color="#000001")
                    self.Table.insert("", "end", values=riga)
                    
            self.Label_ID_Del = ctk.CTkLabel(self.Work_Frame, text="DIGITA ID DA VISUALIZZARE:", font=("Arial", 20),fg_color="transparent", anchor="e")
            self.Label_ID_Del.place(relx=0.02, rely=0.80, anchor="w")
            pywinstyles.set_opacity(self.Label_ID_Del, color="#000001")
                
            self.entry_ID_Del = ctk.CTkEntry(self.Work_Frame, placeholder_text="Id",font=("Arial",20),fg_color="transparent")
            self.entry_ID_Del.place(relx=0.30, rely=0.80, anchor="w", relwidth=0.30)
            pywinstyles.set_opacity(self.entry_ID_Del, color="#000001")
            
            self.button_DEL = ctk.CTkButton(self.Work_Frame, text="📋VISUALIZZA SCHEDA", command=self.Window_User, font=("Arial", 20), fg_color="#1E2229", text_color="WHITE")
            self.button_DEL.place(relx=0.63, rely=0.80, anchor="w", relwidth=0.30)
            pywinstyles.set_opacity(self.button_DEL, value=0.5, color="#1E2229")
        else:
             self.Label_Error.configure(text="UTENTE NON PRESENTE NEL DATABASE", text_color="RED")  
             
    def Update_User_Data_Fun(self):
        Id=self.entry_ID_Del.get()
        Nome=self.entry_name_Show.get()
        Cognome=self.entry_Last_name_Show.get()
        Password=self.entry_PSW_Show.get()
        Privilegio = self.Priv_Value.get()
        Email=self.entry_EMAIL_Show.get()
        Cellulare=self.entry_CELL_Show.get()
        Tessera=self.entry_CARD_Show.get()
        Foto=self.foto_percorso
        
        campi_obbligatori = [self.entry_name_Show, self.entry_Last_name_Show, self.entry_EMAIL_Show, self.entry_CARD_Show]
        tutti_compilati = all(widget.get().strip() != "" for widget in campi_obbligatori) and Privilegio != ""
        
        if not tutti_compilati:
            self.label_Error_Show.configure(text="ATTENZIONE: DEVI INSERIRE TUTTI I DATI OBBLIGATORI", text_color="RED")
            return
        
        if self.sistema.Check_Login_User_To_Add(Nome,Cognome):
            if Password == "":
                self.sistema.Update_User_Data_NO_PSW(Id,Nome, Cognome, Privilegio, Email, Cellulare, Tessera, Foto)
                self.label_Error_Show.configure(text="AGGIORNATO CON SUCCESSO!", text_color="GREEN")
            else:
                self.sistema.Update_User_Data_And_PSW(Id,Nome, Cognome, Password, Privilegio, Email, Cellulare, Tessera, Foto)
                self.label_Error_Show.configure(text="AGGIORNATO CON SUCCESSO!", text_color="GREEN")
        else:
            self.label_Error_Show.configure(text="NOME UTENTE NON VALIDO",text_color="RED")    
        
    def Window_User(self):
        
        self.Window_User_data = ctk.CTkToplevel(fg_color="BLACK")
        
        #===========SETTING WINDOW===================================================================
        self.Window_User_data.title("ARES")
        self.Window_User_data.geometry("1414x752")
        
        self.Show_Window_User_data()
        
        id_cercato = self.entry_ID_Del.get()
        dati = self.sistema.get_user_by_id(id_cercato)
        if dati:
            self.entry_name_Show.insert(0, dati[1])
            self.entry_Last_name_Show.insert(0, dati[2])
            self.entry_PSW_Show.configure(placeholder_text="Lascia vuoto per non modificare")
            self.entry_EMAIL_Show.insert(0, dati[4])
            self.entry_CELL_Show.insert(0, dati[5])
            self.entry_CARD_Show.insert(0, dati[6])
            self.Priv_Value.set(dati[7])
            foto = self.Label_photo_Show.cget("image")
            if dati[8]:
                self.foto_percorso = dati[8]
                img = Image.open(self.foto_percorso)
                foto = ctk.CTkImage(img, size=(200, 250))
                self.Label_photo_Show.configure(image=foto, text="")
                self.Label_photo_Show.image = foto
            
    def Show_Window_User_data(self):
        self.Window_User_frame_login=ctk.CTkFrame(self.Window_User_data)
        self.Window_User_frame_login.place(relx=0.5, rely=0.5, anchor="center",relheight=1,relwidth=1)
        #========================== USER WINDOW WIDGET PRE-COMP ==============================
        self.Title_Add = ctk.CTkLabel(self.Window_User_frame_login, text="MODIFICA DATI NECESSARI", font=("Arial", 40),bg_color="#000001")
        self.Title_Add.place(relx=0.5, rely=0.06, anchor="center")
        pywinstyles.set_opacity(self.Title_Add, color="#000001")
        
        self.Label_name_Show = ctk.CTkLabel(self.Window_User_frame_login, text="NOME:", font=("Arial", 20),bg_color="#000001", anchor="e")
        self.Label_name_Show.place(relx=0.02, rely=0.20, anchor="w")
        pywinstyles.set_opacity(self.Label_name_Show, color="#000001")
        
        self.entry_name_Show = ctk.CTkEntry(self.Window_User_frame_login, placeholder_text="Nome",font=("Arial",20),bg_color="#000001")
        self.entry_name_Show.place(relx=0.15, rely=0.20, anchor="w", relwidth=0.30)
        pywinstyles.set_opacity(self.entry_name_Show, color="#000001")
        
        self.Label_Last_name_Show = ctk.CTkLabel(self.Window_User_frame_login, text="COGNOME:", font=("Arial", 20),bg_color="#000001", anchor="e")
        self.Label_Last_name_Show.place(relx=0.02, rely=0.35, anchor="w")
        pywinstyles.set_opacity(self.Label_Last_name_Show, color="#000001")
        
        self.entry_Last_name_Show = ctk.CTkEntry(self.Window_User_frame_login, placeholder_text="Cognome",font=("Arial",20),bg_color="#000001")
        self.entry_Last_name_Show.place(relx=0.15, rely=0.35, anchor="w", relwidth=0.30)
        pywinstyles.set_opacity(self.entry_Last_name_Show, color="#000001")
        
        self.Label_PSW_Show = ctk.CTkLabel(self.Window_User_frame_login, text="PASSWORD:", font=("Arial", 20),bg_color="#000001", anchor="e")
        self.Label_PSW_Show.place(relx=0.02, rely=0.50,anchor="w")
        pywinstyles.set_opacity(self.Label_PSW_Show, color="#000001")
        
        self.entry_PSW_Show = ctk.CTkEntry(self.Window_User_frame_login, placeholder_text="Password",font=("Arial",20),bg_color="#000001")
        self.entry_PSW_Show.place(relx=0.15, rely=0.50, anchor="w", relwidth=0.30)
        pywinstyles.set_opacity(self.entry_PSW_Show, color="#000001")
        
        self.Label_EMAIL_Show = ctk.CTkLabel(self.Window_User_frame_login, text="EMAIL:", font=("Arial", 20),bg_color="#000001", anchor="e")
        self.Label_EMAIL_Show.place(relx=0.02, rely=0.65,anchor="w")
        pywinstyles.set_opacity(self.Label_EMAIL_Show, color="#000001")
        
        self.entry_EMAIL_Show = ctk.CTkEntry(self.Window_User_frame_login, placeholder_text="Email",font=("Arial",20),bg_color="#000001")
        self.entry_EMAIL_Show.place(relx=0.15, rely=0.65, anchor="w", relwidth=0.30)
        pywinstyles.set_opacity(self.entry_EMAIL_Show, color="#000001")
        
        self.Label_CELL_Show = ctk.CTkLabel(self.Window_User_frame_login, text="CELLULARE:", font=("Arial", 20),bg_color="#000001", anchor="e")
        self.Label_CELL_Show.place(relx=0.02, rely=0.80,anchor="w")
        pywinstyles.set_opacity(self.Label_CELL_Show, color="#000001")
        
        self.entry_CELL_Show = ctk.CTkEntry(self.Window_User_frame_login, placeholder_text="Cellulare",font=("Arial",20),bg_color="#000001")
        self.entry_CELL_Show.place(relx=0.15, rely=0.80, anchor="w", relwidth=0.30)
        pywinstyles.set_opacity(self.entry_CELL_Show, color="#000001")
        
        self.Label_CARD_Show = ctk.CTkLabel(self.Window_User_frame_login, text="N°TESSERA:", font=("Arial", 20),bg_color="#000001", anchor="e")
        self.Label_CARD_Show.place(relx=0.50, rely=0.80,anchor="w")
        pywinstyles.set_opacity(self.Label_CARD_Show, color="#000001")
        
        self.entry_CARD_Show = ctk.CTkEntry(self.Window_User_frame_login, placeholder_text="N°Tessera",font=("Arial",20),bg_color="#000001")
        self.entry_CARD_Show.place(relx=0.63, rely=0.80, anchor="w", relwidth=0.30)
        pywinstyles.set_opacity(self.entry_CARD_Show, color="#000001")
        
        self.Label_PRIV_Show = ctk.CTkLabel(self.Window_User_frame_login, text="PRIVILEGIO:", font=("Arial", 20),bg_color="#000001", anchor="e")
        self.Label_PRIV_Show.place(relx=0.50, rely=0.65,anchor="w")
        pywinstyles.set_opacity(self.Label_PRIV_Show, color="#000001")
        
        self.Priv_Value = ctk.StringVar(value="")
        self.Priv_button_1 = ctk.CTkRadioButton(self.Window_User_frame_login, text="Admin", variable= self.Priv_Value, value="Admin")
        self.Priv_button_1.place(relx=0.65, rely=0.65, anchor="w", relwidth=0.30)
        self.Priv_button_2 = ctk.CTkRadioButton(self.Window_User_frame_login, text="User", variable= self.Priv_Value, value="User")
        self.Priv_button_2.place(relx=0.80, rely=0.65, anchor="w", relwidth=0.30)
        
        self.button_SAVE_Show = ctk.CTkButton(self.Window_User_frame_login, text="AGGIORNA", command=self.Update_User_Data_Fun,font=("Arial black",20),text_color="WHITE",fg_color="#1E2229")
        self.button_SAVE_Show.place(relx=0.75, rely=0.935, anchor="center", relwidth=0.5,relheight=0.125)
        pywinstyles.set_opacity(self.button_SAVE_Show,value=0.5, color="#1E2229")
        
        self.button_Reset_Show = ctk.CTkButton(self.Window_User_frame_login, text="RESET", command=self.Clear_Entry_Window,font=("Arial black",20),text_color="WHITE",fg_color="#1E2229")
        self.button_Reset_Show.place(relx=0.5, rely=0.935, anchor="e", relwidth=0.5,relheight=0.125)
        pywinstyles.set_opacity(self.button_Reset_Show,value=0.5, color="#1E2229")
        
        self.label_Error_Show = ctk.CTkLabel(self.Window_User_frame_login, text="", font=("Arial", 20),bg_color="#000001")
        self.label_Error_Show.place(relx=0.5, rely=0.13, anchor="center")
        pywinstyles.set_opacity(self.label_Error_Show, color="#000001")
        
        self.label_Error_Window2 = ctk.CTkLabel(self.Window_User_frame_login, text="", font=("Arial", 20),bg_color="#000001")
        self.label_Error_Window2.place(relx=0.5, rely=0.13, anchor="center")
        pywinstyles.set_opacity(self.label_Error_Window2, color="#000001")
        #======================= SETTING PHOTO==================
        self.foto_percorso = None
    
        self.Label_FOTO_Show = ctk.CTkLabel(self.Window_User_frame_login, text="FOTO:", font=("Arial", 20), bg_color="#000001", anchor="e")
        self.Label_FOTO_Show.place(relx=0.50, rely=0.35, anchor="w")
        pywinstyles.set_opacity(self.Label_FOTO_Show, color="#000001")
        
        self.button_FOTO_Show = ctk.CTkButton(self.Window_User_frame_login, text="📁 MODIFICA FOTO", command=lambda: self.Carica_Foto(self.Label_photo_Show), font=("Arial", 20), fg_color="#1E2229", text_color="WHITE")
        self.button_FOTO_Show.place(relx=0.60, rely=0.50, anchor="w", relwidth=0.30)
        pywinstyles.set_opacity(self.button_FOTO_Show, value=0.5, color="#1E2229")
        
        self.Label_photo_Show = ctk.CTkLabel(self.Window_User_frame_login, text="Nessuna foto", fg_color="#1E2229", corner_radius=8)
        self.Label_photo_Show.place(relx=0.75, rely=0.29, anchor="center", relwidth=0.30, relheight=0.50)
        pywinstyles.set_opacity(self.Label_photo_Show, value=0.5, color="#1E2229")
    
    def Search_User_Menu(self):
        for widget in self.Work_Frame.winfo_children():
            widget.destroy()
        Vista_db=self.sistema.show_database()
        #============================================= WIDGET ================================================================
        self.Title_Add = ctk.CTkLabel(self.Work_Frame, text="LISTA UTENTI REGISTRATI", font=("Arial", 40),fg_color="transparent")
        self.Title_Add.place(relx=0.5, rely=0.06, anchor="center")
        pywinstyles.set_opacity(self.Title_Add, color="#000001")
        
        self.Title_Add = ctk.CTkLabel(self.Work_Frame, text="INSERISCI DATI DELL'UTENTE DA CERCARE", font=("Arial", 40),fg_color="transparent")
        self.Title_Add.place(relx=0.5, rely=0.06, anchor="center")
        pywinstyles.set_opacity(self.Title_Add, color="#000001")
            
        self.Label_name_Search = ctk.CTkLabel(self.Work_Frame, text="NOME:", font=("Arial", 20),fg_color="transparent", anchor="e")
        self.Label_name_Search.place(relx=0.02, rely=0.13, anchor="w")
        pywinstyles.set_opacity(self.Label_name_Search, color="#000001")
            
        self.entry_name_Search = ctk.CTkEntry(self.Work_Frame, placeholder_text="Nome",font=("Arial",20),fg_color="transparent")
        self.entry_name_Search.place(relx=0.15, rely=0.13, anchor="w", relwidth=0.30)
        pywinstyles.set_opacity(self.entry_name_Search, color="#000001")
            
        self.Label_Last_name_Search = ctk.CTkLabel(self.Work_Frame, text="COGNOME:", font=("Arial", 20),fg_color="transparent", anchor="e")
        self.Label_Last_name_Search.place(relx=0.50, rely=0.13, anchor="w")
        pywinstyles.set_opacity(self.Label_Last_name_Search, color="#000001")
            
        self.entry_Last_name_Search = ctk.CTkEntry(self.Work_Frame, placeholder_text="Cognome",font=("Arial",20),fg_color="transparent")
        self.entry_Last_name_Search.place(relx=0.63, rely=0.13, anchor="w", relwidth=0.30)
        pywinstyles.set_opacity(self.entry_Last_name_Search, color="#000001")
        
        self.Label_info = ctk.CTkLabel(self.Work_Frame, text="PUOI INSERIRE ANCHE SOLO IL N° DI TESSERAMENTO", font=("Arial", 20),fg_color="transparent")
        self.Label_info.place(relx=0.47, rely=0.25, anchor="w")
        pywinstyles.set_opacity(self.Label_info, color="#000001")
        
        self.Label_Error = ctk.CTkLabel(self.Work_Frame, text="", font=("Arial", 20),bg_color="#000001")
        self.Label_Error.place(relx=0.5, rely=0.19, anchor="center")
        pywinstyles.set_opacity(self.Label_Error, color="#000001")
        
        self.Label_NTessera_Search = ctk.CTkLabel(self.Work_Frame, text="N°TESSERA:", font=("Arial", 20),fg_color="transparent", anchor="e")
        self.Label_NTessera_Search.place(relx=0.02, rely=0.25, anchor="w")
        pywinstyles.set_opacity(self.Label_NTessera_Search, color="#000001")
            
        self.entry_NTessera_Search = ctk.CTkEntry(self.Work_Frame, placeholder_text="N°Tessera",font=("Arial",20),fg_color="transparent")
        self.entry_NTessera_Search.place(relx=0.15, rely=0.25, anchor="w", relwidth=0.30)
        pywinstyles.set_opacity(self.entry_NTessera_Search, color="#000001")
        
        self.button_SEARCH = ctk.CTkButton(self.Work_Frame, text="🔍 FILTRA", command=self.Search_User_Menu_Fun, font=("Arial", 20), fg_color="#1E2229", text_color="WHITE")
        self.button_SEARCH.place(relx=0.30, rely=0.30, anchor="w", relwidth=0.30)
        pywinstyles.set_opacity(self.button_SEARCH, value=0.5, color="#1E2229")
    
    
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",background="#1E2229",foreground="white",fieldbackground="#1E2229",rowheight=30)
        style.configure("Treeview.Heading",background="#14171A",foreground="white")
        self.TableSearch = ttk.Treeview(self.Work_Frame, columns=("ID", "Nome", "Cognome","Email","Cellulare","N° Tessera", "Privilegio","Foto" ), show="headings")
        self.TableSearch.heading("ID", text="ID")
        self.TableSearch.heading("Nome", text="Nome")
        self.TableSearch.heading("Cognome", text="Cognome")
        self.TableSearch.heading("Email", text="Email")
        self.TableSearch.heading("Cellulare", text="Cellulare")
        self.TableSearch.column("Cellulare", width=80)
        self.TableSearch.heading("N° Tessera", text="N° Tessera")
        self.TableSearch.column("N° Tessera", width=80)
        self.TableSearch.heading("Privilegio", text="Privilegio")
        self.TableSearch.column("Privilegio", width=75)
        self.TableSearch.heading("Foto", text="Foto")
        self.TableSearch.place(relx=0.5, rely=0.65, anchor="center", relwidth=0.9, relheight=0.5)
        for riga in Vista_db:
            self.TableSearch.insert("", "end", values=riga)
            
    def Search_User_Menu_Fun(self):
        for i in self.TableSearch.get_children():
            self.TableSearch.delete(i)
        Nome_Cercato=self.entry_name_Search.get()
        Cognome_Cercato=self.entry_Last_name_Search.get()
        N_Tessera_cercata=self.entry_NTessera_Search.get()
        
        risultati = self.sistema.search_user_del(Nome_Cercato, Cognome_Cercato)
        risultato_tessera=self.sistema.search_user_del_Tessera(N_Tessera_cercata)
        

        if risultati:
            for riga in risultati:
                self.Label_Error.configure(text="",bg_color="#000001")
                self.TableSearch.insert("", "end", values=riga)
        elif risultato_tessera:
            for riga in risultato_tessera:
                self.Label_Error.configure(text="",bg_color="#000001")
                self.TableSearch.insert("", "end", values=riga)
        else:
            self.Label_Error.configure(text="UTENTE NON PRESENTE NEL DATABASE", text_color="RED")  
            
    def Modify_personal_Data(self):
        for widget in self.Work_Frame.winfo_children():
            widget.destroy()
            
        self.Title_Add = ctk.CTkLabel(self.Work_Frame, text="MODIFICA I TUOI DATI", font=("Arial", 40),bg_color="#000001")
        self.Title_Add.place(relx=0.5, rely=0.06, anchor="center")
        pywinstyles.set_opacity(self.Title_Add, color="#000001")
        
        self.Label_name_Mod = ctk.CTkLabel(self.Work_Frame, text="NOME:", font=("Arial", 20),bg_color="#000001", anchor="e")
        self.Label_name_Mod.place(relx=0.02, rely=0.20, anchor="w")
        pywinstyles.set_opacity(self.Label_name_Mod, color="#000001")
        
        self.entry_name_Mod = ctk.CTkEntry(self.Work_Frame, placeholder_text="Nome",font=("Arial",20),bg_color="#000001")
        self.entry_name_Mod.place(relx=0.15, rely=0.20, anchor="w", relwidth=0.30)
        pywinstyles.set_opacity(self.entry_name_Mod, color="#000001")
        
        self.Label_Last_name_Mod= ctk.CTkLabel(self.Work_Frame, text="COGNOME:", font=("Arial", 20),bg_color="#000001", anchor="e")
        self.Label_Last_name_Mod.place(relx=0.02, rely=0.35, anchor="w")
        pywinstyles.set_opacity(self.Label_Last_name_Mod, color="#000001")
        
        self.entry_Last_name_Mod = ctk.CTkEntry(self.Work_Frame, placeholder_text="Cognome",font=("Arial",20),bg_color="#000001")
        self.entry_Last_name_Mod.place(relx=0.15, rely=0.35, anchor="w", relwidth=0.30)
        pywinstyles.set_opacity(self.entry_Last_name_Mod, color="#000001")
        
        self.Label_PSW_Mod = ctk.CTkLabel(self.Work_Frame, text="PASSWORD:", font=("Arial", 20),bg_color="#000001", anchor="e")
        self.Label_PSW_Mod.place(relx=0.02, rely=0.50,anchor="w")
        pywinstyles.set_opacity(self.Label_PSW_Mod, color="#000001")
        
        self.entry_PSW_Mod = ctk.CTkEntry(self.Work_Frame, placeholder_text="Password",font=("Arial",20),bg_color="#000001")
        self.entry_PSW_Mod.place(relx=0.15, rely=0.50, anchor="w", relwidth=0.30)
        pywinstyles.set_opacity(self.entry_PSW_Mod, color="#000001")
        
        self.Label_EMAIL_Mod = ctk.CTkLabel(self.Work_Frame, text="EMAIL:", font=("Arial", 20),bg_color="#000001", anchor="e")
        self.Label_EMAIL_Mod.place(relx=0.02, rely=0.65,anchor="w")
        pywinstyles.set_opacity(self.Label_EMAIL_Mod, color="#000001")
        
        self.entry_EMAIL_Mod = ctk.CTkEntry(self.Work_Frame, placeholder_text="Email",font=("Arial",20),bg_color="#000001")
        self.entry_EMAIL_Mod.place(relx=0.15, rely=0.65, anchor="w", relwidth=0.30)
        pywinstyles.set_opacity(self.entry_EMAIL_Mod, color="#000001")
        
        self.Label_CELL_Mod= ctk.CTkLabel(self.Work_Frame, text="CELLULARE:", font=("Arial", 20),bg_color="#000001", anchor="e")
        self.Label_CELL_Mod.place(relx=0.02, rely=0.80,anchor="w")
        pywinstyles.set_opacity(self.Label_CELL_Mod, color="#000001")
        
        self.entry_CELL_Mod= ctk.CTkEntry(self.Work_Frame, placeholder_text="Cellulare",font=("Arial",20),bg_color="#000001")
        self.entry_CELL_Mod.place(relx=0.15, rely=0.80, anchor="w", relwidth=0.30)
        pywinstyles.set_opacity(self.entry_CELL_Mod, color="#000001")
        
        self.Label_CARD_Mod= ctk.CTkLabel(self.Work_Frame, text="N°TESSERA:", font=("Arial", 20),bg_color="#000001", anchor="e")
        self.Label_CARD_Mod.place(relx=0.50, rely=0.80,anchor="w")
        pywinstyles.set_opacity(self.Label_CARD_Mod, color="#000001")
        
        self.entry_CARD_Mod = ctk.CTkEntry(self.Work_Frame, placeholder_text="N°Tessera",font=("Arial",20),bg_color="#000001")
        self.entry_CARD_Mod.place(relx=0.63, rely=0.80, anchor="w", relwidth=0.30)
        pywinstyles.set_opacity(self.entry_CARD_Mod, color="#000001")
        
        self.Label_PRIV_Mod = ctk.CTkLabel(self.Work_Frame, text="PRIVILEGIO:", font=("Arial", 20),bg_color="#000001", anchor="e")
        self.Label_PRIV_Mod.place(relx=0.50, rely=0.65,anchor="w")
        pywinstyles.set_opacity(self.Label_PRIV_Mod, color="#000001")
        
        self.Priv_Value_Mod = ctk.StringVar(value="")
        self.Priv_button_1 = ctk.CTkRadioButton(self.Work_Frame, text="Admin", variable= self.Priv_Value_Mod, value="Admin")
        self.Priv_button_1.place(relx=0.65, rely=0.65, anchor="w", relwidth=0.30)
        self.Priv_button_2 = ctk.CTkRadioButton(self.Work_Frame, text="User", variable= self.Priv_Value_Mod, value="User")
        self.Priv_button_2.place(relx=0.80, rely=0.65, anchor="w", relwidth=0.30)
        
        self.button_SAVE_Mod = ctk.CTkButton(self.Work_Frame, text="AGGIORNA", command=self.Update_Personal_Data_Fun,font=("Arial black",20),text_color="WHITE",fg_color="#1E2229")
        self.button_SAVE_Mod.place(relx=0.5, rely=0.935, anchor="center", relwidth=1,relheight=0.125)
        pywinstyles.set_opacity(self.button_SAVE_Mod,value=0.5, color="#1E2229")
        
        self.label_Error_Mod = ctk.CTkLabel(self.Work_Frame, text="", font=("Arial", 20),bg_color="#000001")
        self.label_Error_Mod.place(relx=0.5, rely=0.13, anchor="center")
        pywinstyles.set_opacity(self.label_Error_Mod, color="#000001")
        
        self.label_Error_Window2_Mod = ctk.CTkLabel(self.Work_Frame, text="", font=("Arial", 20),bg_color="#000001")
        self.label_Error_Window2_Mod.place(relx=0.5, rely=0.13, anchor="center")
        pywinstyles.set_opacity(self.label_Error_Window2_Mod, color="#000001")
        
        #======================= SETTING PHOTO==================
        self.foto_percorso = None
    
        self.Label_FOTO_Mod = ctk.CTkLabel(self.Work_Frame, text="FOTO:", font=("Arial", 20), bg_color="#000001", anchor="e")
        self.Label_FOTO_Mod.place(relx=0.50, rely=0.35, anchor="w")
        pywinstyles.set_opacity(self.Label_FOTO_Mod, color="#000001")
        
        self.button_FOTO_Mod = ctk.CTkButton(self.Work_Frame, text="📁 MODIFICA FOTO", command=lambda: self.Carica_Foto(self.Label_photo_Mod), font=("Arial", 20), fg_color="#1E2229", text_color="WHITE")
        self.button_FOTO_Mod.place(relx=0.60, rely=0.50, anchor="w", relwidth=0.30)
        pywinstyles.set_opacity(self.button_FOTO_Mod, value=0.5, color="#1E2229")
        
        self.Label_photo_Mod = ctk.CTkLabel(self.Work_Frame, text="Nessuna foto", fg_color="#1E2229", corner_radius=8)
        self.Label_photo_Mod.place(relx=0.75, rely=0.29, anchor="center", relwidth=0.30, relheight=0.50)
        pywinstyles.set_opacity(self.Label_photo_Mod, value=0.5, color="#1E2229")
        
        self.Modify_personal_PSW_Fun()
        
    def Modify_personal_PSW_Fun(self):
        nome=self.Nome_Loggato
        dati_mod = self.sistema.Select_User(nome)
        if dati_mod:
            self.entry_name_Mod.insert(0, dati_mod[1])
            self.entry_Last_name_Mod.insert(0, dati_mod[2])
            self.entry_PSW_Mod.configure(placeholder_text="Lascia vuoto per non modificare")
            self.Priv_Value_Mod.set(dati_mod[4])
            self.entry_EMAIL_Mod.insert(0, dati_mod[5])
            self.entry_CELL_Mod.insert(0, dati_mod[6])
            self.entry_CARD_Mod.insert(0, dati_mod[7])
            foto = self.Label_photo_Mod.cget("image")
            if dati_mod[8]:
                self.foto_percorso = dati_mod[8]
                img = Image.open(self.foto_percorso)
                foto = ctk.CTkImage(img, size=(200, 250))
                self.Label_photo_Mod.configure(image=foto, text="")
                self.Label_photo_Mod.image = foto
                
    def Update_Personal_Data_Fun(self):
        Nome=self.entry_name_Mod.get()
        Cognome=self.entry_Last_name_Mod.get()
        Password=self.entry_PSW_Mod.get()
        Privilegio = self.Priv_Value_Mod.get()
        Email=self.entry_EMAIL_Mod.get()
        Cellulare=self.entry_CELL_Mod.get()
        Tessera=self.entry_CARD_Mod.get()
        Foto=self.foto_percorso
        Utente=self.Nome_Loggato
        campi_obbligatori = [self.entry_name_Mod, self.entry_Last_name_Mod, self.entry_EMAIL_Mod, self.entry_CELL_Mod]
        tutti_compilati = all(widget.get().strip() != "" for widget in campi_obbligatori) and Privilegio != ""
        
        if not tutti_compilati:
            self.label_Error_Mod.configure(text="ATTENZIONE: DEVI INSERIRE TUTTI I DATI OBBLIGATORI", text_color="RED")
            return
        
        if self.sistema.Check_Login_User_To_Add(Nome,Cognome):
            if Password == "":
               self.sistema.Update_Personal_Data_NO_PSW(Nome, Cognome, Privilegio, Email, Cellulare, Tessera, Foto, Utente)
               self.label_Error_Window2_Mod.configure(text="AGGIORNATO CON SUCCESSO!", text_color="GREEN")
            else:
                self.sistema.Update_Personal_Data_And_PSW(Nome,Cognome,Password,Privilegio,Email,Cellulare,Tessera,Foto,Utente)
                self.label_Error_Window2_Mod.configure(text="AGGIORNATO CON SUCCESSO!", text_color="GREEN")
        else:
            self.label_Error_Window2_Mod.configure(text="NOME UTENTE NON VALIDO", text_color="RED")
    
    def Window_PSW_FRG(self,event=None):
        
        self.Window_PSW = ctk.CTkToplevel(fg_color="BLACK")
        
        #===========SETTING WINDOW===================================================================
        self.Window_PSW.title("RESET PASSWORD")
        self.Window_PSW.geometry("650x400")
        self.Window_PSW.grab_set()
        
        self.Show_Window_PSW_FRG()
    
    def Show_Window_PSW_FRG(self):
        self.Window_PSW_FRG_frame=ctk.CTkFrame(self.Window_PSW)
        self.Window_PSW_FRG_frame.place(relx=0.5, rely=0.5, anchor="center",relheight=1,relwidth=1)
        
        self.Title_Add = ctk.CTkLabel(self.Window_PSW_FRG_frame, text="INSERISCI DATI PER IL RESET", font=("Arial", 40),bg_color="#000001")
        self.Title_Add.place(relx=0.5, rely=0.06, anchor="center")
        pywinstyles.set_opacity(self.Title_Add, color="#000001")
        
        self.Label_name_PSW = ctk.CTkLabel(self.Window_PSW_FRG_frame, text="NOME:", font=("Arial", 20),bg_color="#000001", anchor="e")
        self.Label_name_PSW.place(relx=0.02, rely=0.20, anchor="w")
        pywinstyles.set_opacity(self.Label_name_PSW, color="#000001")
        
        self.entry_name_PSW = ctk.CTkEntry(self.Window_PSW_FRG_frame, placeholder_text="Nome",font=("Arial",20),bg_color="#000001")
        self.entry_name_PSW.place(relx=0.15, rely=0.20, anchor="w", relwidth=0.30)
        pywinstyles.set_opacity(self.entry_name_PSW, color="#000001")
        
        self.Label_Last_name_PSW = ctk.CTkLabel(self.Window_PSW_FRG_frame, text="COGNOME:", font=("Arial", 20),bg_color="#000001", anchor="e")
        self.Label_Last_name_PSW.place(relx=0.50, rely=0.20, anchor="w")
        pywinstyles.set_opacity(self.Label_Last_name_PSW, color="#000001")
        
        self.entry_Last_name_PSW = ctk.CTkEntry(self.Window_PSW_FRG_frame, placeholder_text="Cognome",font=("Arial",20),bg_color="#000001")
        self.entry_Last_name_PSW.place(relx=0.70, rely=0.20, anchor="w", relwidth=0.30)
        pywinstyles.set_opacity(self.entry_Last_name_PSW, color="#000001")
        
        self.Label_CARD_PSW = ctk.CTkLabel(self.Window_PSW_FRG_frame, text="N°TESSERA:", font=("Arial", 20),bg_color="#000001", anchor="e")
        self.Label_CARD_PSW.place(relx=0.25, rely=0.30,anchor="w")
        pywinstyles.set_opacity(self.Label_CARD_PSW, color="#000001")
        
        self.entry_CARD_PSW = ctk.CTkEntry(self.Window_PSW_FRG_frame, placeholder_text="N°Tessera",font=("Arial",20),bg_color="#000001")
        self.entry_CARD_PSW.place(relx=0.45, rely=0.30, anchor="w", relwidth=0.30)
        pywinstyles.set_opacity(self.entry_CARD_PSW, color="#000001")
        
        self.Label_PSW = ctk.CTkLabel(self.Window_PSW_FRG_frame, text="NUOVA PASSWORD:", font=("Arial", 20),bg_color="#000001", anchor="e")
        self.Label_PSW.place(relx=0.02, rely=0.50,anchor="w")
        pywinstyles.set_opacity(self.Label_PSW, color="#000001")
        
        self.entry_PSW = ctk.CTkEntry(self.Window_PSW_FRG_frame, placeholder_text="Nuova Password",font=("Arial",20),bg_color="#000001")
        self.entry_PSW.place(relx=0.35, rely=0.50, anchor="w", relwidth=0.30)
        pywinstyles.set_opacity(self.entry_PSW, color="#000001")
        
        self.Label_PSW_Conf = ctk.CTkLabel(self.Window_PSW_FRG_frame, text="RIPETI PASSWORD:", font=("Arial", 20),bg_color="#000001", anchor="e")
        self.Label_PSW_Conf.place(relx=0.02, rely=0.70,anchor="w")
        pywinstyles.set_opacity(self.Label_PSW_Conf, color="#000001")
        
        self.entry_PSW_Conf = ctk.CTkEntry(self.Window_PSW_FRG_frame, placeholder_text="Conferma Password",font=("Arial",20),bg_color="#000001")
        self.entry_PSW_Conf.place(relx=0.35, rely=0.70, anchor="w", relwidth=0.30)
        pywinstyles.set_opacity(self.entry_PSW_Conf, color="#000001")
        
        self.label_Error_WindowPSW = ctk.CTkLabel(self.Window_PSW_FRG_frame, text="", font=("Arial", 20),bg_color="#000001")
        self.label_Error_WindowPSW.place(relx=0.5, rely=0.40, anchor="center")
        pywinstyles.set_opacity(self.label_Error_WindowPSW, color="#000001")
        
        self.button_SAVE_PSW = ctk.CTkButton(self.Window_PSW_FRG_frame, text="RESET", command=self.Reset_PSW_FRG,font=("Arial black",20),text_color="WHITE",fg_color="#1E2229")
        self.button_SAVE_PSW.place(relx=0.5, rely=0.93, anchor="center", relwidth=1,relheight=0.2)
        pywinstyles.set_opacity(self.button_SAVE_PSW,value=0.5, color="#1E2229")
        
    def Reset_PSW_FRG(self):
        Nome=self.entry_name_PSW.get()
        Cognome=self.entry_Last_name_PSW.get()
        Tessera=self.entry_CARD_PSW.get()
        Password1=self.entry_PSW.get()
        Password2=self.entry_PSW_Conf.get()
    
        if Password1==Password2:
            if self.sistema.Reset_Password(Nome, Cognome, Tessera, Password2):
                self.label_Error_WindowPSW.configure(text="",bg_color="#000001")
                self.label_Error_WindowPSW.configure(text="PASSWORD AGGIORNATA",text_color="GREEN")
            else:
                self.label_Error_WindowPSW.configure(text="DATI INSERITI ERRATI",text_color="RED")
        else:
            self.label_Error_WindowPSW.configure(text="LE PASSWORD DEVONO ESSERE UGUALI")
    
if __name__ == "__main__":
   app = AresGUI()