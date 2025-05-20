import tkinter as tk # GUI-Bibliothek
from tkinter import messagebox # Dialoge

# zeigt das Passwort an oder verbirgt es
def toggle_password():
    if password_entry.cget('show') == '':
        password_entry.config(show='*')
        show_password_var.set(0)
    else:
        password_entry.config(show='')
        show_password_var.set(1)

# --- Hauptfenster ---
def show_main_page():
    main_page = tk.Toplevel(root)
    main_page.title("Passwort Manager - User: " + username_entry.get())
    center_window(main_page, 600, 280)

    main_page.lift()  # Hauptseite in den Vordergrund bringen
    main_page.focus_force()  # Fokus auf Hauptseite setzen
    root.withdraw()

    # --- Logout-Funktion ---
    def logout():
        main_page.destroy()
        root.deiconify()

    # --- Fenster schließen ---
    def on_main_page_close():
        main_page.destroy()
        root.deiconify()

    main_page.protocol("WM_DELETE_WINDOW", on_main_page_close)

    # --- Passwort hinzufügen ---
    add_frame = tk.Frame(main_page)
    add_frame.pack(pady=20)

    # Eingabefelder für Seite und Passwort
    site_label = tk.Label(add_frame, text="Seite:")
    site_label.grid(row=0, column=0, padx=5)
    site_entry = tk.Entry(add_frame, width=20)
    site_entry.grid(row=0, column=1, padx=5)

    pw_label = tk.Label(add_frame, text="Passwort:")
    pw_label.grid(row=0, column=2, padx=5)
    pw_entry = tk.Entry(add_frame, width=20, show='*')
    pw_entry.grid(row=0, column=3, padx=5)

    # Seite & Passwort hinzufügen
    def add_password():
        site = site_entry.get()
        pw = pw_entry.get()
        if not site or not pw:
            messagebox.showwarning("Fehler", "Bitte Seite und Passwort angeben.")
            return
        password_list.append((site, pw)) # Passwort zur Liste hinzufügen
        update_password_list()
        site_entry.delete(0, tk.END)
        pw_entry.delete(0, tk.END)

    plus_button = tk.Button(add_frame, text="+", command=add_password, width=3)
    plus_button.grid(row=0, column=4, padx=5)

    # Passwort-Liste
    password_list = []
    list_frame = tk.Frame(main_page)
    list_frame.pack(pady=(0, 10))
    listbox = tk.Listbox(list_frame, width=60)
    listbox.pack()

    def update_password_list():
        listbox.delete(0, tk.END)
        for site, pw in password_list:
            listbox.insert(tk.END, f"Seite: {site}   |   Passwort: {'*' * len(pw)}")

    # Passwort-Liste aktualisieren
    def on_listbox_double_click(event):
        selection = listbox.curselection()
        if not selection:
            return
        index = selection[0]
        site, pw = password_list[index]

        edit_window = tk.Toplevel(main_page)
        edit_window.title("Passwort bearbeiten")
        center_window(edit_window, 350, 200)

        site_label = tk.Label(edit_window, text="Seite:")
        site_label.pack(pady=(15, 0), anchor="w", padx=20)

        # Eingabefeld für die Seite
        site_entry_edit = tk.Entry(edit_window, width=30)
        site_entry_edit.pack(anchor="w", padx=20)
        site_entry_edit.insert(0, site)

        # Eingabefeld für das Passwort (standardmäßig mit *)
        pw_label = tk.Label(edit_window, text="Passwort:")
        pw_label.pack(pady=(10, 0), anchor="w", padx=20)
        pw_entry_edit = tk.Entry(edit_window, width=30, show='*')
        pw_entry_edit.pack(anchor="w", padx=20)
        pw_entry_edit.insert(0, pw)

        # Checkbox zum Anzeigen/Verbergen des Passworts
        show_pw_var = tk.IntVar()
        def toggle_edit_password():
            if show_pw_var.get():
                pw_entry_edit.config(show='')
            else:
                pw_entry_edit.config(show='*')
        show_pw_check = tk.Checkbutton(edit_window, text="Passwort zeigen", variable=show_pw_var, command=toggle_edit_password)
        show_pw_check.pack(anchor="w", padx=20)

        # Button zum Kopieren des Passworts in die Zwischenablage
        def copy_password():
            edit_window.clipboard_clear()
            edit_window.clipboard_append(pw_entry_edit.get())
            edit_window.update()
        copy_button = tk.Button(edit_window, text="Kopieren", command=copy_password, width=10)
        copy_button.pack(anchor="w", padx=20)

        # Speichern der Änderungen
        def save_changes():
            new_site = site_entry_edit.get()
            new_pw = pw_entry_edit.get()
            if not new_site or not new_pw:
                messagebox.showwarning("Fehler", "Bitte Seite und Passwort angeben.")
                return
            password_list[index] = (new_site, new_pw)
            update_password_list()
            edit_window.destroy()

        # Löschen des Eintrags
        def delete_entry():
            del password_list[index]
            update_password_list()
            edit_window.destroy()

        button_frame = tk.Frame(edit_window)
        button_frame.pack(pady=15)
        save_button = tk.Button(button_frame, text="Speichern", command=save_changes, width=12)
        save_button.pack(side="left", padx=5)
        delete_button = tk.Button(button_frame, text="Löschen", command=delete_entry, width=10)
        delete_button.pack(side="left", padx=5)

    listbox.bind('<Double-Button-1>', on_listbox_double_click)

    # Abmelde-Button
    logout_button = tk.Button(main_page, text="Abmelden", command=logout, width=20)
    logout_button.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)
    root.withdraw()

# --- Login-Funktion ---
def login_clicked():
    username = username_entry.get()
    password = password_entry.get()
    if username == "" or password == "":
        messagebox.showwarning("Warnung", "Bitte Benutzername und Passwort eingeben.")
    else:
        show_main_page()

# --- Zentrierung des Fensters ---
def center_window(window, width=300, height=180):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# --- Registrierungsseite ---
def show_register_page():
    root.withdraw()
    register_page = tk.Toplevel(root)
    register_page.title("Registrieren")
    center_window(register_page, 350, 260)

    username_label = tk.Label(register_page, text="Benutzername:")
    username_label.pack(pady=(15, 0), anchor="w", padx=20)
    username_entry = tk.Entry(register_page, width=25)
    username_entry.pack(anchor="w", padx=20)

    password_label = tk.Label(register_page, text="Passwort:")
    password_label.pack(pady=(10, 0), anchor="w", padx=20)
    password_entry = tk.Entry(register_page, show='*', width=25)
    password_entry.pack(anchor="w", padx=20)

    confirm_label = tk.Label(register_page, text="Passwort bestätigen:")
    confirm_label.pack(pady=(10, 0), anchor="w", padx=20)
    confirm_entry = tk.Entry(register_page, show='*', width=25)
    confirm_entry.pack(anchor="w", padx=20)

    show_password_var = tk.IntVar()

    def toggle_register_password():
        if show_password_var.get():
            password_entry.config(show='')
        else:
            password_entry.config(show='*')

    def close_register_page():
        register_page.destroy()
        root.deiconify()

    show_password_check = tk.Checkbutton(register_page, text="Passwörter zeigen", variable=show_password_var, command=toggle_register_password, anchor="w")
    show_password_check.pack(pady=(5, 0), anchor="w", padx=20)

    # Überprüfung der Eingaben
    def register():
        password = password_entry.get()
        confirm = confirm_entry.get()
        if password != confirm:
            messagebox.showerror("Fehler", "Die Passwörter stimmen nicht überein.")
        else:
            messagebox.showinfo("Erfolg", "Registrierung erfolgreich (Platzhalter)")
            register_page.destroy()

    button_frame = tk.Frame(register_page)
    button_frame.pack(pady=15)
    register_button = tk.Button(button_frame, text="Registrieren", command=register, width=12)
    register_button.pack(side="left", padx=5)
    close_button = tk.Button(button_frame, text="Schließen", command=close_register_page, width=10)
    close_button.pack(side="left", padx=5)

    register_page.protocol("WM_DELETE_WINDOW", close_register_page)

root = tk.Tk()
root.title("Passwort Manager")
center_window(root, 300, 180)
root.geometry("300x180")
root.protocol("WM_DELETE_WINDOW", root.destroy)

username_label = tk.Label(root, text="Benutzername:", anchor="w", width=20)
username_label.pack(pady=(15, 0), anchor="w", padx=20)
username_entry = tk.Entry(root, width=25)
username_entry.pack(anchor="w", padx=20)

password_label = tk.Label(root, text="Passwort:", anchor="w", width=20)
password_label.pack(pady=(10, 0), anchor="w", padx=20)
password_entry = tk.Entry(root, show='*', width=25)
password_entry.pack(anchor="w", padx=20)

show_password_var = tk.IntVar()
show_password_check = tk.Checkbutton(root, text="Passwort zeigen", variable=show_password_var, command=toggle_password, anchor="w")
show_password_check.pack(pady=(5, 0), anchor="w", padx=20)

button_frame = tk.Frame(root)
button_frame.pack(pady=15)

login_button = tk.Button(button_frame, text="Login", command=login_clicked, width=10)
login_button.pack(side="left", padx=5)

register_button = tk.Button(button_frame, text="Registrieren", command=show_register_page, width=12)
register_button.pack(side="left", padx=5)

root.mainloop()
