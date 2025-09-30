import tkinter as tk
from tkinter import ttk, messagebox
from data import load_etecs, get_average_rating

class EtecListFrame(tk.Frame):
    def __init__(self, master, on_select_etec):
        super().__init__(master)
        self.master = master
        self.on_select_etec = on_select_etec
        self.etecs = load_etecs()

        self.label = tk.Label(self, text="Lista das Etecs do Estado de São Paulo", font=("Helvetica", 14, "bold"))
        self.label.pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("city", "avg_rating"), show="headings", selectmode="browse")
        self.tree.heading("city", text="Cidade")
        self.tree.heading("avg_rating", text="Avaliação Média")
        self.tree.column("city", width=150)
        self.tree.column("avg_rating", width=120, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.populate_tree()

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Back button
        back_button = tk.Button(self, text="Voltar ao Menu", command=self.master.show_main_menu,
                               bg="#2196F3", fg="white", font=("Helvetica", 10, "bold"))
        back_button.pack(pady=10)

    def populate_tree(self):
        for etec in self.etecs:
            avg_rating = get_average_rating(etec.id)
            self.tree.insert("", "end", iid=etec.id, values=(etec.city, f"{avg_rating:.2f}"))

    def on_tree_select(self, event):
        selected_id = self.tree.selection()
        if selected_id:
            etec_id = int(selected_id[0])
            etec = next((e for e in self.etecs if e.id == etec_id), None)
            if etec:
                self.on_select_etec(etec)
            else:
                messagebox.showerror("Erro", "Etec não encontrada.")
