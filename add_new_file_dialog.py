from os.path import exists, isfile
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk, filedialog
from tkcalendar import DateEntry
from add_new_person import open_add_person
from add_new_sender import open_add_sender
from add_new_tag import open_add_tag
from db_handler import add_file, get_persons, get_tags, add_entry, get_senders
import os

def open_add_dialog(on_ok_callback):
    def on_add_person():
        open_add_person(refill_persons)

    def refill_persons():
        person_combobox['values'] = get_persons()

    def on_add_sender():
        open_add_sender(refill_senders)

    def refill_senders():
        sender_combobox['values'] = get_senders()

    def on_add_tag():
        open_add_tag(tag_added_callback)

    def tag_added_callback():
        nonlocal listbox
        listbox.delete(0, tk.END);
        tags = get_tags()
        for tag in tags:
            listbox.insert(tk.END, tag)

    def showErrorMessage(message):
        messagebox.showerror(title="Fehler", message=message, parent=dialog)

    def select_file():
        file_path = filedialog.askopenfilename(
            title="Datei auswählen", 
            filetypes=[("Alle Dateien", "*.*"), ("Textdateien", "*.txt")],
            parent=dialog
        )
        if file_path:
            file_entry.delete(0, tk.END)
            file_entry.insert(0, file_path)

    def on_ok():
        person_input = person_combobox.get()
        file_path = file_entry.get()
        name = name_entry.get().strip()

        if not os.path.exists(file_path):
            showErrorMessage("Die angegebene Datei existiert nicht")
            return
        if not os.path.isfile(file_path):
            showErrorMessage("Der angegebene Pfad zeigt nicht auf eine Datei.")
            return
        if name == "":
            showErrorMessage("Bitte geben Sie einen namen für den Eintrag an")
            return
        if( person_input == "" ):
            messagebox.showerror(title="Fehler", message="Bitte wähle eine Person aus.", parent=dialog)
            return

        print( "person: " + person_input)
        selected_tags = [listbox.get(i) for i in listbox.curselection()]
        fileId = add_file(file_path)
        add_entry(date_picker.get_date(), person_input, sender_combobox.get(), name, note_text.get("1.0", tk.END).strip(), selected_tags, fileId )
        on_ok_callback()
        dialog.destroy()

    dialog = tk.Toplevel()
    dialog.title("Datei Hinzufügen")

    dialog.transient();
    dialog.grab_set();

    tk.Label(dialog, text="Dateipfad:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
    file_entry = tk.Entry(dialog, width=40)
    file_entry.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
    tk.Button(dialog, text="Datei auswählen", command=select_file).grid(row=0, column=2, padx=10, pady=5, sticky='ew')

    tk.Label(dialog, text="Name:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
    name_entry = tk.Entry(dialog, width=40)
    name_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky='ew')

    tk.Label(dialog, text="Datum:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
    date_picker = DateEntry(dialog, width=12, background='darkblue', foreground='white', borderwidth=2)
    date_picker.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    tk.Label(dialog, text="Person:").grid(row=3, column=0, padx=10, pady=5, sticky='w')
    persons = get_persons()
    person_combobox = ttk.Combobox(dialog, values=persons, state="readonly")
    person_combobox.grid(row=3, column=1, columnspan=1, padx=10, pady=5, sticky='ew')
    
    tk.Button(dialog, text="Person hinzufügen", command=on_add_person).grid(row=3, column=2, padx=10, pady=10, sticky='ew')

    tk.Label(dialog, text="Absender:").grid(row=4, column=0, padx=10, pady=5, sticky='w')
    senders = get_senders()
    sender_combobox = ttk.Combobox(dialog, values=senders, state="readonly")
    sender_combobox.grid(row=4, column=1, columnspan=1, padx=10, pady=5, sticky='ew')
    
    tk.Button(dialog, text="Absender hinzufügen", command=on_add_sender).grid(row=4, column=2, padx=10, pady=10)

    tk.Label(dialog, text="Notiz:").grid(row=5, column=0, padx=10, pady=5, sticky='nw')
    note_text = tk.Text(dialog, width=40, height=5)
    note_text.grid(row=5, column=1, columnspan=2, padx=10, pady=5, sticky='ew')

    tk.Label(dialog, text="Tags:").grid(row=6, column=0, padx=10, pady=5, sticky="nw")
    tags = get_tags()
    listbox = tk.Listbox(dialog, selectmode=tk.MULTIPLE, height=8)
    listbox.grid(row=6, column=1, padx=10, pady=5, sticky='ew')
    for tag in tags:
        listbox.insert(tk.END, tag)

    tk.Button(dialog, text="Tag hinzufügen", command=on_add_tag).grid(row=6, column=2, padx=10, pady=10, sticky="new")

    buttonFrame = tk.Frame(dialog)
    buttonFrame.grid(row=7, column=1, columnspan=3, padx=10, pady=5)
    okButton = tk.Button(buttonFrame, text="Datei hinzufügen", command=on_ok)
    okButton.grid(row=1, column=1, pady=10, padx=10)

    cancelButton = tk.Button(buttonFrame, text="Abbrechen", command=dialog.destroy)
    cancelButton.grid(row=1, column=2, pady=10, padx=10)

    dialog.wait_window();
