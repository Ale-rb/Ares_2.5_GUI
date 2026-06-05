# Ares 2.5 - User Management System

**Ares 2.5** is a Python-based user management system. This version represents a significant evolution from the previous console-based versions, now featuring a modern graphical user interface (GUI) developed with **CustomTkinter** and enhanced visual aesthetics through advanced transparency handling.

---

### IT

**Ares 2.5** è un sistema gestionale per l'accesso utenti sviluppato in Python. Questa versione integra un'interfaccia grafica moderna (GUI) sviluppata con **CustomTkinter** e introduce un impatto visivo rifinito grazie alla gestione avanzata delle trasparenze dei widget tramite **pywinstyles**, mantenendo la persistenza dei dati su database relazionale **SQLite**.

---

## 🚀 Main Features / Funzionalità Principali

* **Modern GUI / Interfaccia Moderna**: A sleek and responsive dark-themed interface built using CustomTkinter widgets and custom glass/transparency window styles.
* **Profile Management / Gestione Profili**: Complete forms to view, update, or clear personal records including role assignments (ADMIN/USER), card numbers, and profile pictures.
* **Advanced Database Search / Ricerca Avanzata**: Efficient user filtering via custom search queries visualized inside a dynamic hierarchical `Treeview` component.
* **Password Reset Window / Finestra Ripristino Credenziali**: A secure, isolated window allowing users or supervisors to safely reset access credentials after passing a cross-verification check.

## 🛠️ Tech Stack

* **Language**: Python 3.x
* **Database**: SQLite3
* **Libraries**: 
    * `customtkinter` (for the modern dark-themed UI)
    * `pywinstyles` (for windows transparency and styling hacks)
    * `Pillow` (for dynamic profile picture loading and scaling)

---

## 💻 How to Run / Come Avviare

```bash
# Install dependencies / Installa le dipendenze
pip install customtkinter pywinstyles Pillow

# Clone and run the app / Clona e avvia l'applicazione
git clone [https://github.com/Ale-rb/Ares_2.5_GUI.git](https://github.com/Ale-rb/Ares_2.5_GUI.git)
cd Ares_2.5_GUI
python main.py
