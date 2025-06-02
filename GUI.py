import tkinter as tk
from tkinter import messagebox

from Backend.Utils.DBManager import DBManager
from Backend.Utils.Encryption import Encryption
from Backend.ProgramSettings import ProgramSettings
from Backend.Utils.ToolHelper import ToolHelper
from Backend.Utils.PasswordSafety import PasswordSafety
from Backend.Utils.PasswordGeneration import PasswordGeneration


def center_window(window, width=300, height=180):
    """
    Center the given window on the screen.

    Args:
        window (tk.Tk or tk.Toplevel): The window to center.
        width (int): Width of the window.
        height (int): Height of the window.
    """
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


class GUI:
    """
    Main GUI class for the password manager.
    Manages all user interactions and windows.
    """

    def __init__(self, dbManager: DBManager, encryption: Encryption, toolHelper: ToolHelper,
                 passwordSafety: PasswordSafety, passwordGeneration: PasswordGeneration):
        """
        Initialize GUI and dependencies.
        """
        self.db = dbManager
        self.encryption = encryption
        self.toolHelper = toolHelper
        self.passwordSafety = passwordSafety
        self.passwordGeneration = passwordGeneration
        self.show_password_var = None
        self.password_entry = None
        self.root = tk.Tk()
        self.root.title("Passwort Manager")
        center_window(self.root, 350, 200)
        self.password_list = []
        self.show_login_page()
        self.root.mainloop()

    def show_login_page(self):
        """
        Display the login screen.
        """
        self.root.deiconify()
        for widget in self.root.winfo_children():
            widget.destroy()

        label = tk.Label(self.root, text="Passwort eingeben:")
        label.pack(pady=(30, 5))

        self.password_entry = tk.Entry(self.root, show='*', width=25)
        self.password_entry.pack(pady=(0, 5))

        self.show_password_var = tk.IntVar(value=0)
        show_pw = tk.Checkbutton(self.root, text="Passwort zeigen", variable=self.show_password_var,
                                 command=self.toggle_password)
        show_pw.pack()

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        login_btn = tk.Button(button_frame, text="Login", command=self.login_clicked)
        login_btn.pack(side="left", padx=5)

    def toggle_password(self):
        """
        Toggle password visibility in the entry field.
        """
        self.password_entry.config(show='' if self.show_password_var.get() else '*')

    def login_clicked(self):
        """
        Handle login button click event.
        Validate the entered password against stored password.
        """
        password = self.password_entry.get()
        if password == "":
            messagebox.showwarning("Warnung", "Bitte Passwort eingeben.")
        else:
            db_user_password = self.db.tableSaves_GetSave(1)
            db_user_password = self.encryption.Decrypt(db_user_password)
            if password == db_user_password:
                ProgramSettings.CRYPT_KEY = db_user_password
                self.password_list = self.toolHelper.GetDecryptedPWList()
                self.show_main_page()
            else:
                messagebox.showwarning("Falsches Passwort", "Das eingegebene Passwort ist nicht korrekt!")

    def show_main_page(self):
        """
        Display the main page after successful login.
        """
        main_page = tk.Toplevel(self.root)
        main_page.title("Passwort Manager")
        center_window(main_page, 600, 420)
        main_page.lift()
        main_page.focus_force()
        self.root.withdraw()

        main_page.protocol("WM_DELETE_WINDOW", lambda: self.on_main_page_close(main_page))

        # Top area with input fields and generate button
        add_frame = tk.Frame(main_page)
        add_frame.pack(pady=20, fill='x')

        site_label = tk.Label(add_frame, text="Seite:")
        site_label.grid(row=0, column=0, padx=5)
        site_entry = tk.Entry(add_frame, width=20)
        site_entry.grid(row=0, column=1, padx=5)

        pw_label = tk.Label(add_frame, text="Passwort:")
        pw_label.grid(row=0, column=2, padx=5)
        pw_entry = tk.Entry(add_frame, width=20, show='*')
        pw_entry.grid(row=0, column=3, padx=5)

        length_label = tk.Label(add_frame, text="Länge:")
        length_label.grid(row=1, column=2, sticky="w", padx=5, pady=(5, 0))
        length_slider = tk.Scale(add_frame, from_=8, to=32, orient=tk.HORIZONTAL)
        length_slider.grid(row=1, column=3, sticky="w", padx=5, pady=(5, 0))

        generate_button = tk.Button(add_frame, text="Generieren",
                                    command=lambda: self.generate_password(length_slider.get(), pw_entry),
                                    width=10)
        generate_button.grid(row=1, column=4, sticky="w", padx=5, pady=(5, 0))

        plus_button = tk.Button(add_frame, text="+",
                                command=lambda: self.add_password(site_entry, pw_entry,
                                                                  lambda: self.update_password_list(self.listbox)),
                                width=3)
        plus_button.grid(row=0, column=5, padx=5)

        # Listbox with scrollbar
        content_frame = tk.Frame(main_page)
        content_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        list_frame = tk.Frame(content_frame)
        list_frame.pack(fill='both', expand=True)

        scrollbar = tk.Scrollbar(list_frame, orient='vertical')
        self.listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side='right', fill='y')
        self.listbox.pack(side='left', fill='both', expand=True)

        self.update_password_list(self.listbox)
        self.listbox.bind('<Double-Button-1>', lambda event: self.on_listbox_double_click(self.listbox, main_page))

        # Bottom buttons
        buttons_frame = tk.Frame(content_frame)
        buttons_frame.pack(fill='x')

        logout_button = tk.Button(buttons_frame, text="Abmelden",
                                  command=lambda: self.logout(main_page), width=20)
        logout_button.pack(side='left', anchor='w')

        change_pw_btn = tk.Button(buttons_frame, text="Passwort ändern",
                                  command=lambda: self.open_change_password_page(main_page), width=20)
        change_pw_btn.pack(side='right', anchor='e')

    def generate_password(self, length, pw_entry):
        """
        Generate a password and display it in the password entry.
        """
        generated_password = self.passwordGeneration.Generate(length)
        pw_entry.delete(0, tk.END)
        pw_entry.insert(0, generated_password)

    def open_change_password_page(self, main_page):
        """
        Open the password change dialog.
        """
        change_pw_page = tk.Toplevel(main_page)
        change_pw_page.title("Passwort ändern")
        center_window(change_pw_page, 400, 320)

        # UI elements for password change
        current_label = tk.Label(change_pw_page, text="Aktuelles Passwort:")
        current_label.pack(pady=(20, 0))
        current_entry = tk.Entry(change_pw_page, show='*', width=25)
        current_entry.pack()

        new_label = tk.Label(change_pw_page, text="Neues Passwort:")
        new_label.pack(pady=(10, 0))
        new_entry = tk.Entry(change_pw_page, show='*', width=25)
        new_entry.pack()

        # Password generator area
        length_gen_frame = tk.Frame(change_pw_page)
        length_gen_frame.pack(anchor="w", padx=20, pady=(5, 0), fill='x')

        length_label = tk.Label(length_gen_frame, text="Länge:")
        length_label.pack(side="left")

        length_slider = tk.Scale(length_gen_frame, from_=8, to=32, orient=tk.HORIZONTAL)
        length_slider.pack(side="left", padx=(5, 10))

        generate_button = tk.Button(length_gen_frame, text="Generieren", width=10)
        generate_button.pack(side="left")

        def generate_in_edit():
            self.generate_password(length_slider.get(), new_entry)
        generate_button.config(command=generate_in_edit)

        confirm_label = tk.Label(change_pw_page, text="Neues Passwort bestätigen:")
        confirm_label.pack(pady=(10, 0))
        confirm_entry = tk.Entry(change_pw_page, show='*', width=25)
        confirm_entry.pack()

        show_pw_var = tk.IntVar()

        def toggle_pw():
            show = '' if show_pw_var.get() else '*'
            new_entry.config(show=show)
            confirm_entry.config(show=show)

        show_pw = tk.Checkbutton(change_pw_page, text="Passwörter zeigen", variable=show_pw_var, command=toggle_pw)
        show_pw.pack()

        button_frame = tk.Frame(change_pw_page)
        button_frame.pack(pady=10)

        def change_password():
            current_password = current_entry.get()
            new_password = new_entry.get()
            confirm = confirm_entry.get()

            db_user_password = self.db.tableSaves_GetSave(1)
            db_user_password = self.encryption.Decrypt(db_user_password)

            if current_password != db_user_password:
                messagebox.showwarning("Fehler", "Aktuelles Passwort ist falsch.")
                return
            if not new_password or not confirm:
                messagebox.showwarning("Fehler", "Bitte alle Felder ausfüllen.")
                return
            if new_password != confirm:
                messagebox.showwarning("Fehler", "Neue Passwörter stimmen nicht überein.")
                return

            if self.toolHelper.UpdateUserPassword(new_password):
                self.password_list = self.toolHelper.GetDecryptedPWList()
                self.update_password_list(self.listbox)
                messagebox.showinfo("Erfolg", "Passwort wurde geändert.")
            else:
                messagebox.showerror("Fehler", "Das Passwort konnte nicht geändert werden!")

            change_pw_page.destroy()

        def cancel():
            change_pw_page.destroy()

        change_btn = tk.Button(button_frame, text="Ändern", command=change_password)
        change_btn.pack(side="left", padx=5)

        cancel_btn = tk.Button(button_frame, text="Abbrechen", command=cancel)
        cancel_btn.pack(side="left", padx=5)

        change_pw_page.protocol("WM_DELETE_WINDOW", change_pw_page.destroy)

    def logout(self, main_page):
        """
        Logout and return to the login page.
        """
        if messagebox.askyesno("Abmelden", "Wirklich abmelden?"):
            main_page.destroy()
            self.root.deiconify()

    def on_main_page_close(self, main_page):
        """
        Handle closing of main window.
        """
        main_page.destroy()
        self.root.deiconify()

    def add_password(self, site_entry, pw_entry, update_password_list):
        """
        Add a new password to the list and database.
        """
        site = site_entry.get()
        pw = pw_entry.get()

        if not site or not pw:
            messagebox.showwarning("Fehler", "Bitte Seite und Passwort angeben.")
            return

        if not self.passwordSafety.Check(pw):
            return

        if self.db.tableValues_GetValue(site) != "":
            messagebox.showwarning("Fehler", "Dieses Feld existiert bereits!")
            return

        password_encrypted = self.encryption.Encrypt(pw)
        self.db.tableValues_CreateValue(site, password_encrypted)

        self.password_list.append((site, pw))
        update_password_list()
        site_entry.delete(0, tk.END)
        pw_entry.delete(0, tk.END)

    def update_password_list(self, listbox):
        """
        Update the password list shown in the listbox.
        """
        listbox.delete(0, tk.END)
        for site, pw in self.password_list:
            listbox.insert(tk.END, f"Seite: {site}   |   Passwort: {'*' * len(pw)}")

    def on_listbox_double_click(self, listbox, main_page):
        """
        Handle double click on a listbox item to edit/delete password.
        """
        selection = listbox.curselection()
        if not selection:
            return

        index = selection[0]
        site, pw = self.password_list[index]
        edit_window = tk.Toplevel(main_page)
        edit_window.title("Passwort bearbeiten")
        center_window(edit_window, 400, 250)

        site_label = tk.Label(edit_window, text="Seite:")
        site_label.pack(pady=(15, 0), anchor="w", padx=20)
        site_value_label = tk.Label(edit_window, text=site, width=30, anchor="w", justify="left")
        site_value_label.pack(anchor="w", padx=20)

        pw_label = tk.Label(edit_window, text="Passwort:")
        pw_label.pack(pady=(10, 0), anchor="w", padx=20)
        pw_entry_edit = tk.Entry(edit_window, width=30, show='*')
        pw_entry_edit.pack(anchor="w", padx=20)
        pw_entry_edit.insert(0, pw)

        length_gen_frame = tk.Frame(edit_window)
        length_gen_frame.pack(anchor="w", padx=20, pady=(5, 0), fill='x')

        length_label = tk.Label(length_gen_frame, text="Länge:")
        length_label.pack(side="left")

        length_slider = tk.Scale(length_gen_frame, from_=8, to=32, orient=tk.HORIZONTAL)
        length_slider.pack(side="left", padx=(5, 10))

        generate_button = tk.Button(length_gen_frame, text="Generieren", width=10)
        generate_button.pack(side="left")

        def generate_in_edit():
            self.generate_password(length_slider.get(), pw_entry_edit)
        generate_button.config(command=generate_in_edit)

        show_pw_var = tk.IntVar()

        def toggle_edit_password():
            pw_entry_edit.config(show='' if show_pw_var.get() else '*')

        show_pw_check = tk.Checkbutton(edit_window, text="Passwort zeigen", variable=show_pw_var,
                                       command=toggle_edit_password)
        show_pw_check.pack(anchor="w", padx=20)

        def copy_password():
            edit_window.clipboard_clear()
            edit_window.clipboard_append(pw_entry_edit.get())
            edit_window.update()

        copy_button = tk.Button(edit_window, text="Kopieren", command=copy_password, width=10)
        copy_button.pack(anchor="w", padx=20)

        def save_changes():
            site = site_value_label.cget("text")
            new_pw = pw_entry_edit.get()

            if not new_pw:
                messagebox.showwarning("Fehler", "Bitte Passwort angeben.")
                return

            if self.db.tableValues_SaveValue(site, self.encryption.Encrypt(new_pw)):
                self.password_list[index] = (site, new_pw)
                self.update_password_list(listbox)
                messagebox.showinfo("Erfolg", "Die Änderung wurde erfolgreich gespeichert")
            else:
                messagebox.showerror("Fehler", "Die Änderung konnte nicht gespeichert werden")
            edit_window.destroy()

        def delete_entry():
            site = self.password_list[index][0]

            if self.db.tableValues_DeleteValue(site):
                del self.password_list[index]
                self.update_password_list(listbox)
                messagebox.showinfo("Erfolg", "Der Eintrag wurde erfolgreich gelöscht.")
            else:
                messagebox.showerror("Fehler", "Der Eintrag konnte nicht gelöscht werden!")
            edit_window.destroy()

        button_frame = tk.Frame(edit_window)
        button_frame.pack(pady=15)

        save_button = tk.Button(button_frame, text="Speichern", command=save_changes, width=12)
        save_button.pack(side="left", padx=5)

        delete_button = tk.Button(button_frame, text="Löschen", command=delete_entry, width=10)
        delete_button.pack(side="left", padx=5)
