import tkinter as tk
from tkinter import ttk, filedialog
from tkcalendar import DateEntry
from add_new_person import open_add_person
from add_new_tag import open_add_tag
from db_handler import add_file, get_persons, get_tags, add_entry

def open_add_dialog(on_ok_callback):
    def on_add_person():
        open_add_person(refill_persons)

    def refill_persons():
        person_combobox['values'] = get_persons()

    def on_add_tag():
        open_add_tag(tag_added_callback)

    def tag_added_callback(tagName):
        nonlocal row, tag_vars
        tag_vars[tagName] = tk.BooleanVar();
        tk.Checkbutton(dialog, text=tagName, variable=tag_vars[tagName]).grid(row=row, column=1, sticky="w", padx=10, pady=2)
        row += 1
        okButton.grid(row=row, column=1, pady=10)
        cancelButton.grid(row=row, column=2, pady=10)


    def select_file():
        file_path = filedialog.askopenfilename(
            title="Datei auswählen", 
            filetypes=[("Alle Dateien", "*.*"), ("Textdateien", "*.txt")]
        )
        if file_path:
            file_entry.delete(0, tk.END)
            file_entry.insert(0, file_path)

    def on_ok():
        selected_tags = []
        for tag, var in tag_vars.items():
            if var.get():
                selected_tags.append(tag)
        fileId = add_file(file_entry.get())
        add_entry(date_picker.get_date(), person_combobox.get(), name_entry.get(), note_text.get("1.0", tk.END).strip(), selected_tags, fileId )
        on_ok_callback()
        dialog.destroy()

    dialog = tk.Toplevel()
    dialog.title("Datei Hinzufügen")

    dialog.transient();
    dialog.grab_set();

    tk.Label(dialog, text="Dateipfad:").grid(row=0, column=0, padx=10, pady=5)
    file_entry = tk.Entry(dialog, width=40)
    file_entry.grid(row=0, column=1, padx=10, pady=5)
    tk.Button(dialog, text="Datei auswählen", command=select_file).grid(row=0, column=2, padx=10, pady=5)

    tk.Label(dialog, text="Name:").grid(row=1, column=0, padx=10, pady=5)
    name_entry = tk.Entry(dialog, width=40)
    name_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=5)

    tk.Label(dialog, text="Datum:").grid(row=2, column=0, padx=10, pady=5)
    date_picker = DateEntry(dialog, width=12, background='darkblue', foreground='white', borderwidth=2)
    date_picker.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    tk.Label(dialog, text="Person:").grid(row=3, column=0, padx=10, pady=5)
    persons = get_persons()
    person_combobox = ttk.Combobox(dialog, values=persons, state="readonly")
    person_combobox.grid(row=3, column=1, columnspan=1, padx=10, pady=5)
    
    tk.Button(dialog, text="Neue Person hinzufügen", command=on_add_person).grid(row=3, column=2, padx=10, pady=10)


    tk.Label(dialog, text="Notiz:").grid(row=4, column=0, padx=10, pady=5)
    note_text = tk.Text(dialog, width=40, height=5)
    note_text.grid(row=4, column=1, columnspan=2, padx=10, pady=5)

    tk.Label(dialog, text="Tags:").grid(row=5, column=0, padx=10, pady=5, sticky="nw")
    tags = get_tags()
    tag_vars = {tag: tk.BooleanVar() for tag in tags}
    row = 5
    for i, tag in enumerate(tags):
        tk.Checkbutton(dialog, text=tag, variable=tag_vars[tag]).grid(row=row, column=1, sticky="w", padx=10, pady=2)
        row += 1

    tk.Button(dialog, text="Neuen Tag hinzufügen", command=on_add_tag).grid(row=5, column=2, padx=10, pady=10)
    
    okCancelRow = row;
    if( okCancelRow == 5 ):
        okCancelRow +=1

    okButton = tk.Button(dialog, text="Ok", command=on_ok)
    okButton.grid(row=okCancelRow, column=1, pady=10)

    cancelButton = tk.Button(dialog, text="Schließen", command=dialog.destroy)
    cancelButton.grid(row=okCancelRow, column=2, pady=10)

    dialog.wait_window();
