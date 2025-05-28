import tkinter as tk # GUI-Bibliothek
from tkinter import messagebox # Dialoge

# Funktion zum Zentrieren des Fensters auf dem Bildschirm
def center_window(window, width=300, height=180):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def open_change_password_page(main_page):
    change_pw_page = tk.Toplevel(main_page)
    change_pw_page.title("Passwort ändern")
    
    center_window(change_pw_page, 350, 280)

    current_label = tk.Label(change_pw_page, text="Aktuelles Passwort:")
    current_label.pack(pady=(20, 0))
    current_entry = tk.Entry(change_pw_page, show='*', width=25)
    current_entry.pack()

    new_label = tk.Label(change_pw_page, text="Neues Passwort:")
    new_label.pack(pady=(10, 0))
    new_entry = tk.Entry(change_pw_page, show='*', width=25)
    new_entry.pack()

    confirm_label = tk.Label(change_pw_page, text="Neues Passwort bestätigen:")
    confirm_label.pack(pady=(10, 0))
    confirm_entry = tk.Entry(change_pw_page, show='*', width=25)
    confirm_entry.pack()

    show_pw_var = tk.IntVar()
    
    def toggle_pw():
        show = '' if show_pw_var.get() else '*'
        new_entry.config(show=show)
        
    show_pw = tk.Checkbutton(change_pw_page, text="Passwörter zeigen", variable=show_pw_var, command=toggle_pw)
    show_pw.pack()

    button_frame = tk.Frame(change_pw_page)
    button_frame.pack(pady=10)

    def change_password():
        curr = current_entry.get()
        new = new_entry.get()
        confirm = confirm_entry.get()

        # Hier sollte eine echte Passwortprüfung stattfinden "admin nur ein Platzhalter"
        if curr != "admin":
            messagebox.showwarning("Fehler", "Aktuelles Passwort ist falsch.")
            return
        if not new or not confirm:
            messagebox.showwarning("Fehler", "Bitte alle Felder ausfüllen.")
            return
        if new != confirm:
            messagebox.showwarning("Fehler", "Neue Passwörter stimmen nicht überein.")
            return

        messagebox.showinfo("Erfolg", "Passwort wurde geändert.")
        change_pw_page.destroy()

    def cancel():
        change_pw_page.destroy()

    change_btn = tk.Button(button_frame, text="Ändern", command=change_password)
    change_btn.pack(side="left", padx=5)

    cancel_btn = tk.Button(button_frame, text="Abbrechen", command=cancel)
    cancel_btn.pack(side="left", padx=5)

    def on_close():
        change_pw_page.destroy()

    change_pw_page.protocol("WM_DELETE_WINDOW", on_close)


class GUI:
    # Erstellt das Hauptfenster und initialisiert die GUI
    def __init__(self):
        self.show_password_var = None
        self.password_entry = None
        self.root = tk.Tk()
        self.root.title("Passwort Manager")
        center_window(self.root, 350, 200)
        self.password_list = []
        self.show_login_page()
        self.root.mainloop()

    # Zentriert das Fenster auf dem Bildschirm

    def show_login_page(self):
        self.root.deiconify()
        for widget in self.root.winfo_children():
            widget.destroy()

        # Überschrift für das Login-Fenster
        label = tk.Label(self.root, text="Passwort eingeben:")
        label.pack(pady=(30, 5))

        # Eingabefeld für das Passwort
        self.password_entry = tk.Entry(self.root, show='*', width=25)
        self.password_entry.pack(pady=(0, 5))

        # Checkbox zum Anzeigen/Verbergen des Passworts
        self.show_password_var = tk.IntVar(value=0)
        show_pw = tk.Checkbutton(self.root, text="Passwort zeigen", variable=self.show_password_var, command=self.toggle_password)
        show_pw.pack()

        # Frame für die Login- und Registrieren-Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        # Login-Button
        login_btn = tk.Button(button_frame, text="Login", command=self.login_clicked)
        login_btn.pack(side="left", padx=5)

    def toggle_password(self):
        if self.show_password_var.get():
            self.password_entry.config(show='')
        else:
            self.password_entry.config(show='*')

    def login_clicked(self):
        password = self.password_entry.get()
        if password == "":
            messagebox.showwarning("Warnung", "Bitte Passwort eingeben.")
        else:
            # Hier ggf. Passwortprüfung einbauen
            self.show_main_page()

    def show_main_page(self):
        # Hauptseite mit Passwortverwaltung
        main_page = tk.Toplevel(self.root)
        main_page.title("Passwort Manager")
        center_window(main_page, 600, 280)
        main_page.lift()
        main_page.focus_force()
        self.root.withdraw()

        change_pw_btn = tk.Button(main_page, text="Passwort ändern", command=lambda: open_change_password_page(main_page), width=20)
        change_pw_btn.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

        main_page.protocol("WM_DELETE_WINDOW", lambda: self.on_main_page_close(main_page))

        # Bereich zum Hinzufügen neuer Passwörter
        add_frame = tk.Frame(main_page)
        add_frame.pack(pady=20)

        site_label = tk.Label(add_frame, text="Seite:")
        site_label.grid(row=0, column=0, padx=5)

        site_entry = tk.Entry(add_frame, width=20)
        site_entry.grid(row=0, column=1, padx=5)

        pw_label = tk.Label(add_frame, text="Passwort:")
        pw_label.grid(row=0, column=2, padx=5)

        pw_entry = tk.Entry(add_frame, width=20, show='*')
        pw_entry.grid(row=0, column=3, padx=5)

        plus_button = tk.Button(add_frame, text="+", command=lambda: self.add_password(site_entry, pw_entry, lambda: self.update_password_list(listbox)), width=3)
        plus_button.grid(row=0, column=4, padx=5)

        list_frame = tk.Frame(main_page)
        list_frame.pack(pady=(0, 10))

        listbox = tk.Listbox(list_frame, width=60)
        listbox.pack()

        # Funktion zum Aktualisieren der Passwortliste in der Listbox
        self.update_password_list(listbox)

        # Bindet das Doppelklicken auf die Listbox
        listbox.bind('<Double-Button-1>', lambda event: self.on_listbox_double_click(listbox, main_page))
        logout_button = tk.Button(main_page, text="Abmelden", command=lambda: self.logout(main_page), width=20)
        logout_button.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)

    def logout(self, main_page):
        if messagebox.askyesno("Abmelden", "Wirklich abmelden?"):
            main_page.destroy()
            self.root.deiconify()

    def on_main_page_close(self, main_page):
        main_page.destroy()
        self.root.deiconify()

    def add_password(self, site_entry, pw_entry, update_password_list):
        site = site_entry.get()
        pw = pw_entry.get()

        if not site or not pw:
            messagebox.showwarning("Fehler", "Bitte Seite und Passwort angeben.")
            return

        self.password_list.append((site, pw))
        update_password_list()
        site_entry.delete(0, tk.END)
        pw_entry.delete(0, tk.END)

    def update_password_list(self, listbox):
        listbox.delete(0, tk.END)

        for site, pw in self.password_list:
            listbox.insert(tk.END, f"Seite: {site}   |   Passwort: {'*' * len(pw)}")

    def on_listbox_double_click(self, listbox, main_page):
        selection = listbox.curselection()

        if not selection:
            return

        index = selection[0]
        site, pw = self.password_list[index]
        edit_window = tk.Toplevel(main_page)
        edit_window.title("Passwort bearbeiten")
        center_window(edit_window, 350, 200)

        site_label = tk.Label(edit_window, text="Seite:")
        site_label.pack(pady=(15, 0), anchor="w", padx=20)
        site_entry_edit = tk.Entry(edit_window, width=30)
        site_entry_edit.pack(anchor="w", padx=20)
        site_entry_edit.insert(0, site)

        pw_label = tk.Label(edit_window, text="Passwort:")
        pw_label.pack(pady=(10, 0), anchor="w", padx=20)
        pw_entry_edit = tk.Entry(edit_window, width=30, show='*')
        pw_entry_edit.pack(anchor="w", padx=20)
        pw_entry_edit.insert(0, pw)

        show_pw_var = tk.IntVar()

        def toggle_edit_password():
            if show_pw_var.get():
                pw_entry_edit.config(show='')
            else:
                pw_entry_edit.config(show='*')

        show_pw_check = tk.Checkbutton(edit_window, text="Passwort zeigen", variable=show_pw_var, command=toggle_edit_password)
        show_pw_check.pack(anchor="w", padx=20)

        # Button zum Kopieren des Passworts
        def copy_password():
            edit_window.clipboard_clear()
            edit_window.clipboard_append(pw_entry_edit.get())
            edit_window.update()

        copy_button = tk.Button(edit_window, text="Kopieren", command=copy_password, width=10)
        copy_button.pack(anchor="w", padx=20)

        def save_changes():
            new_site = site_entry_edit.get()
            new_pw = pw_entry_edit.get()

            if not new_site or not new_pw:
                messagebox.showwarning("Fehler", "Bitte Seite und Passwort angeben.")
                return

            self.password_list[index] = (new_site, new_pw)
            self.update_password_list(listbox)
            edit_window.destroy()

        def delete_entry():
            del self.password_list[index]
            self.update_password_list(listbox)
            edit_window.destroy()

        button_frame = tk.Frame(edit_window)
        button_frame.pack(pady=15)

        save_button = tk.Button(button_frame, text="Speichern", command=save_changes, width=12)
        save_button.pack(side="left", padx=5)

        delete_button = tk.Button(button_frame, text="Löschen", command=delete_entry, width=10)
        delete_button.pack(side="left", padx=5)

# Initialisiert die GUI
if __name__ == "__main__":
    GUI()