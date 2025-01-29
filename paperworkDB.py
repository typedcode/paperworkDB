import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from add_new_file_dialog import open_add_dialog
from db_handler import get_tags, init_db, get_entries, get_persons, get_first_date, get_senders
from datetime import datetime

from open_file import readBlobData

init_db()

def new_file():
    open_add_dialog(dialog_ok_callback)

def dialog_ok_callback():
    start_date_picker.set_date(datetime.strptime( get_first_date()[0], '%Y-%m-%d'));
    apply_filters()

def update_selected_tags():
    global selected_tags
    selected_tags = [tag for tag, var in tag_vars.items() if var.get()]
    selected_tags_label.config(text="Ausgewählte Tags: " + ", ".join(selected_tags))
    apply_filters()

def double_click(event):
    item = tree.selection()[0]
    readBlobData(tree.item(item)['values'][6])

def apply_filters(a = None):
    person = person_combobox.get()
    sender = sender_combobox.get()
    start_date = start_date_picker.get_date()
    end_date = end_date_picker.get_date()
    for item in tree.get_children():
        tree.delete(item)

    for row in get_entries():
        row_date = row[1]
        row_person = row[2]
        row_sender = row[3]
        row_tags = [] if row[5] == None else row[5].split(", ")
        
        if (
            (not person or person == row_person) and
            (not sender or sender == row_sender) and
            (not start_date or row_date >= start_date.strftime('%Y-%m-%d')) and
            (not end_date or row_date <= end_date.strftime('%Y-%m-%d')) and
            all(tag in row_tags for tag in selected_tags)
        ):
            tree.insert("", "end", values=row)

root = tk.Tk()
root.title("paperworkDB")

menubar = tk.Menu(root)
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Neu", command=new_file)
menubar.add_cascade(label="Datei", menu=file_menu)
root.config(menu=menubar)

filter_frame = tk.Frame(root)
filter_frame.grid(row=0, column=0, columnspan=2, pady=5, sticky="ew")

person_label = tk.Label(filter_frame, text="Person:")
person_label.grid(row=0, column=0, padx=5, pady=5)
persons = get_persons()
person_combobox = ttk.Combobox(filter_frame, values=persons, state="readonly")
person_combobox.bind('<<ComboboxSelected>>', apply_filters)
person_combobox.grid(row=0, column=1, padx=5, pady=5)

sender_label = tk.Label(filter_frame, text="Absender:")
sender_label.grid(row=0, column=2, padx=5, pady=5)
senders = get_senders()
sender_combobox = ttk.Combobox(filter_frame, values=senders, state="readonly")
sender_combobox.bind('<<ComboboxSelected>>', apply_filters)
sender_combobox.grid(row=0, column=3, padx=5, pady=5)

start_date_label = tk.Label(filter_frame, text="Startdatum:")
start_date_label.grid(row=0, column=4, padx=5, pady=5)
start_date_picker = DateEntry(filter_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
start_date_picker.bind('<<DateEntrySelected>>', apply_filters);
if get_first_date()[0] != None:
    start_date_picker.set_date(datetime.strptime( get_first_date()[0], '%Y-%m-%d'));
start_date_picker.grid(row=0, column=5, padx=5, pady=5)

end_date_label = tk.Label(filter_frame, text="Enddatum:")
end_date_label.grid(row=0, column=6, padx=5, pady=5)
end_date_picker = DateEntry(filter_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
end_date_picker.grid(row=0, column=7, padx=5, pady=5)
end_date_picker.bind('<<DateEntrySelected>>', apply_filters);

tag_frame = tk.Frame(root)
tag_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")

selected_tags_label = tk.Label(tag_frame, text="Ausgewählte Tags: Keine")
selected_tags_label.grid(row=0, column=0, padx=5, pady=5)

tag_button = ttk.Button(tag_frame, text="Tags auswählen")
tag_button.grid(row=0, column=1, padx=5, pady=5)

tags = get_tags()
tag_vars = {tag: tk.BooleanVar() for tag in tags}
selected_tags = []

def show_tag_menu(event):
    tag_menu.post(event.x_root, event.y_root)

tag_menu = tk.Menu(root, tearoff=0)
for tag, var in tag_vars.items():
    tag_menu.add_checkbutton(label=tag, variable=var, onvalue=True, offvalue=False, command=update_selected_tags)

tag_button.bind("<Button-1>", show_tag_menu)

columns = ("Id", "Datum", "Person", "Sender", "Name", "Tags", "Notiz", "FileId")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="w")
tree['displaycolumns'] = ("Datum", "Person", "Sender", "Name", "Tags", "Notiz")

scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
tree.bind('<Double-1>', double_click)

tree.grid(row=2, column=0, sticky="nsew")
scrollbar.grid(row=2, column=1, sticky="ns")

root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

apply_filters()

root.mainloop()

