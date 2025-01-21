import tkinter as tk
from db_handler import add_tag

def open_add_tag(add_tag_callback):
    def on_ok():
        add_tag(tag_entry.get() )
        add_tag_callback(tag_entry.get())
        dialog.destroy()

    dialog = tk.Toplevel()
    dialog.title("Tag Hinzufügen")
    
    dialog.transient();
    dialog.grab_set();

    tk.Label(dialog, text="Tag:").grid(row=0, column=0, padx=10, pady=5)
    tag_entry = tk.Entry(dialog, width=40)
    tag_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=5)

    tk.Button(dialog, text="Ok", command=on_ok).grid(row=1, column=1, pady=10)
    tk.Button(dialog, text="Schließen", command=dialog.destroy).grid(row=1, column=2, pady=10)

    dialog.wait_window();
