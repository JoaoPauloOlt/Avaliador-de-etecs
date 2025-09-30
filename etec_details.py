import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk
import os
from data import Rating, save_ratings, load_ratings

class EtecDetailsFrame(tk.Frame):
    def __init__(self, master, etec, current_user, on_back):
        super().__init__(master)
        self.master = master
        self.etec = etec
        self.current_user = current_user
        self.on_back = on_back

        self.star_buttons = []
        self.selected_rating = 0

        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self, text=f"Avaliação: {self.etec.name}", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        # Photo display
        self.photo_label = tk.Label(self)
        self.photo_label.pack(pady=10)
        self.load_photo()

        # Star rating section
        stars_frame = tk.Frame(self)
        stars_frame.pack(pady=10)

        stars_label = tk.Label(stars_frame, text="Avaliação (estrelas):", font=("Helvetica", 12))
        stars_label.pack()

        stars_container = tk.Frame(stars_frame)
        stars_container.pack()

        for i in range(6):  # 0 to 5 stars
            star_button = tk.Button(stars_container, text=str(i), font=("Helvetica", 14),
                                   command=lambda r=i: self.set_rating(r), width=3)
            star_button.pack(side=tk.LEFT, padx=2)
            self.star_buttons.append(star_button)

        self.update_star_display()

        # Comment section
        comment_label = tk.Label(self, text="Comentário:", font=("Helvetica", 12))
        comment_label.pack(pady=(20, 5))

        self.comment_text = scrolledtext.ScrolledText(self, width=50, height=8, wrap=tk.WORD)
        self.comment_text.pack(pady=5)

        # Buttons
        buttons_frame = tk.Frame(self)
        buttons_frame.pack(pady=20)

        submit_button = tk.Button(buttons_frame, text="Enviar Avaliação", command=self.submit_rating,
                                 bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"))
        submit_button.pack(side=tk.LEFT, padx=10)

        back_button = tk.Button(buttons_frame, text="Voltar", command=self.on_back,
                               bg="#2196F3", fg="white", font=("Helvetica", 10, "bold"))
        back_button.pack(side=tk.LEFT, padx=10)

    def load_photo(self):
        try:
            if os.path.exists(self.etec.photo_path):
                image = Image.open(self.etec.photo_path)
                image = image.resize((300, 200), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.photo_label.config(image=photo)
                self.photo_label.image = photo  # Keep a reference
            else:
                self.photo_label.config(text="[Foto não disponível]", font=("Helvetica", 12))
        except Exception as e:
            self.photo_label.config(text="[Erro ao carregar foto]", font=("Helvetica", 12))
            print(f"Erro ao carregar foto: {e}")

    def set_rating(self, rating):
        self.selected_rating = rating
        self.update_star_display()

    def update_star_display(self):
        for i, button in enumerate(self.star_buttons):
            if i == self.selected_rating:
                button.config(bg="gold", fg="black")
            else:
                button.config(bg="white", fg="black")

    def submit_rating(self):
        comment = self.comment_text.get("1.0", tk.END).strip()

        if self.selected_rating == 0 and not comment:
            messagebox.showwarning("Aviso", "Por favor, forneça uma avaliação ou comentário.")
            return

        # Check if user already rated this Etec
        ratings = load_ratings()
        existing_rating = next((r for r in ratings if r.etec_id == self.etec.id and r.username == self.current_user.username), None)

        if existing_rating:
            # Update existing rating
            existing_rating.stars = self.selected_rating
            existing_rating.comment = comment
        else:
            # Create new rating
            new_rating = Rating(self.etec.id, self.current_user.username, self.selected_rating, comment)
            ratings.append(new_rating)

        save_ratings(ratings)
        messagebox.showinfo("Sucesso", "Avaliação enviada com sucesso!")
        self.on_back()
