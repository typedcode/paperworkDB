import tkinter as tk
from db_handler import add_person

def open_add_person(add_person_callback):
    def on_ok():
        add_person(name_entry.get() )
        add_person_callback()
        dialog.destroy()

    dialog = tk.Toplevel()
    dialog.title("Person Hinzufügen")
    
    dialog.transient();
    dialog.grab_set();

    tk.Label(dialog, text="Name:").grid(row=0, column=0, padx=10, pady=5)
    name_entry = tk.Entry(dialog, width=40)
    name_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=5)

    tk.Button(dialog, text="Ok", command=on_ok).grid(row=1, column=1, pady=10)
    tk.Button(dialog, text="Schließen", command=dialog.destroy).grid(row=1, column=2, pady=10)

    dialog.wait_window();
