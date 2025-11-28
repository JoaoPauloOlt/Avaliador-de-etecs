import tkinter as tk
from tkinter import ttk, scrolledtext
from data import load_ratings, get_average_rating, load_etecs

class BlogFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.label = tk.Label(self, text="Blog de Avaliações das Etecs", font=("Helvetica", 12, "bold"))
        self.label.pack(pady=10)

        filter_frame = tk.Frame(self)
        filter_frame.pack(pady=5)

        filter_label = tk.Label(filter_frame, text="Filtrar por Etec:", font=("Helvetica", 8))
        filter_label.pack(side=tk.LEFT, padx=5)

        self.etec_var = tk.StringVar()
        self.etec_var.set("Todas")

        etecs = ["Todas"] + [etec.name for etec in load_etecs()]
        self.etec_combo = ttk.Combobox(filter_frame, textvariable=self.etec_var, values=etecs, state="readonly")
        self.etec_combo.pack(side=tk.LEFT, padx=5)
        self.etec_combo.bind("<<ComboboxSelected>>", self.update_display)

        self.text_area = scrolledtext.ScrolledText(self, width=40, height=15, wrap=tk.WORD, font=("Helvetica", 8))
        self.text_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.text_area.config(state=tk.DISABLED)

        buttons_frame = tk.Frame(self)
        buttons_frame.pack(pady=10)

        reload_button = tk.Button(buttons_frame, text="Recarregar", command=self.update_display,
                                 bg="#FF9800", fg="white", font=("Helvetica", 8, "bold"))
        reload_button.pack(side=tk.LEFT, padx=10)

        back_button = tk.Button(buttons_frame, text="Voltar ao Menu", command=self.master.show_main_menu,
                               bg="#2196F3", fg="white", font=("Helvetica", 8, "bold"))
        back_button.pack(side=tk.LEFT, padx=10)

        self.update_display()

    def update_display(self, event=None):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)

        selected_etec = self.etec_var.get()
        etecs = load_etecs()
        ratings = load_ratings()

        if selected_etec == "Todas":
            for etec in etecs:
                etec_ratings = [r for r in ratings if r.etec_id == etec.id]
                if etec_ratings:
                    avg_rating = get_average_rating(etec.id)
                    self.text_area.insert(tk.END, f" {etec.name} ({etec.city})\n", "etec_title")
                    self.text_area.insert(tk.END, f"Avaliação média: {avg_rating:.2f} estrelas\n\n", "avg_rating")

                    for rating in sorted(etec_ratings, key=lambda x: x.date, reverse=True):
                        stars = "⭐" * rating.stars if rating.stars > 0 else "Sem estrelas"
                        date_str = rating.date.strftime("%d/%m/%Y %H:%M") if rating.date else "Data desconhecida"
                        self.text_area.insert(tk.END, f"Usuário: {rating.username} | {stars} | {date_str}\n", "rating_header")
                        if rating.comment:
                            self.text_area.insert(tk.END, f"Comentário: {rating.comment}\n", "comment")
                        self.text_area.insert(tk.END, "-" * 50 + "\n\n", "separator")
        else:
            # Show ratings for selected Etec
            etec = next((e for e in etecs if e.name == selected_etec), None)
            if etec:
                etec_ratings = [r for r in ratings if r.etec_id == etec.id]
                avg_rating = get_average_rating(etec.id)
                self.text_area.insert(tk.END, f" {etec.name} ({etec.city})\n", "etec_title")
                self.text_area.insert(tk.END, f"Avaliação média: {avg_rating:.2f} estrelas\n\n", "avg_rating")

                if etec_ratings:
                    for rating in sorted(etec_ratings, key=lambda x: x.date, reverse=True):
                        stars = "⭐" * rating.stars if rating.stars > 0 else "Sem estrelas"
                        date_str = rating.date.strftime("%d/%m/%Y %H:%M") if rating.date else "Data desconhecida"
                        self.text_area.insert(tk.END, f"Usuário: {rating.username} | {stars} | {date_str}\n", "rating_header")
                        if rating.comment:
                            self.text_area.insert(tk.END, f"Comentário: {rating.comment}\n", "comment")
                        self.text_area.insert(tk.END, "-" * 50 + "\n\n", "separator")
                else:
                    self.text_area.insert(tk.END, "Nenhuma avaliação encontrada para esta Etec.\n", "no_ratings")

        self.text_area.tag_config("etec_title", font=("Helvetica", 12, "bold"), foreground="blue")
        self.text_area.tag_config("avg_rating", font=("Helvetica", 10, "italic"), foreground="green")
        self.text_area.tag_config("rating_header", font=("Helvetica", 10, "bold"))
        self.text_area.tag_config("comment", font=("Helvetica", 10))
        self.text_area.tag_config("separator", foreground="gray")
        self.text_area.tag_config("no_ratings", font=("Helvetica", 10, "italic"), foreground="red")

        self.text_area.config(state=tk.DISABLED)
