import tkinter as tk
from db_handler import add_sender

def open_add_sender(add_sender_callback):
    def on_ok():
        add_sender(sender_text.get("1.0", tk.END).strip())
        add_sender_callback()
        dialog.destroy()

    dialog = tk.Toplevel()
    dialog.title("Person Hinzufügen")
    
    dialog.transient();
    dialog.grab_set();

    tk.Label(dialog, text="Name:").grid(row=0, column=0, padx=10, pady=5)

    sender_text = tk.Text(dialog, width=40, height=5)
    sender_text.grid(row=0, column=1, columnspan=2, padx=10, pady=5)

    tk.Button(dialog, text="Ok", command=on_ok).grid(row=1, column=1, pady=10)
    tk.Button(dialog, text="Schließen", command=dialog.destroy).grid(row=1, column=2, pady=10)

    dialog.wait_window();
