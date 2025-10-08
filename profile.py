import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
from data import User, load_users, save_users

class ProfileFrame(tk.Frame):
    def __init__(self, master, current_user, on_back):
        super().__init__(master)
        self.master = master
        self.current_user = current_user
        self.on_back = on_back

        self.photo_image = None
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self, text="Perfil do Usuário", font=("Helvetica", 12, "bold"))
        title_label.pack(pady=10)

        # Photo section
        photo_frame = tk.Frame(self)
        photo_frame.pack(pady=10)

        self.photo_label = tk.Label(photo_frame, text="[Sem foto]", font=("Helvetica", 10))
        self.photo_label.pack()

        change_photo_button = tk.Button(photo_frame, text="Alterar Foto", command=self.change_photo, font=("Helvetica", 8))
        change_photo_button.pack(pady=5)

        self.load_user_photo()

        # User info section
        info_frame = tk.Frame(self)
        info_frame.pack(pady=10, padx=10, fill=tk.X)

        # Username (read-only)
        username_label = tk.Label(info_frame, text="Usuário:", font=("Helvetica", 8, "bold"))
        username_label.grid(row=0, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(info_frame, width=20)
        self.username_entry.insert(0, self.current_user.username)
        self.username_entry.config(state="readonly")
        self.username_entry.grid(row=0, column=1, pady=5, padx=(10, 0))

        # Name
        name_label = tk.Label(info_frame, text="Nome:", font=("Helvetica", 8, "bold"))
        name_label.grid(row=1, column=0, sticky="w", pady=5)
        self.name_entry = tk.Entry(info_frame, width=20)
        self.name_entry.insert(0, self.current_user.name)
        self.name_entry.grid(row=1, column=1, pady=5, padx=(10, 0))

        # Email
        email_label = tk.Label(info_frame, text="Email:", font=("Helvetica", 8, "bold"))
        email_label.grid(row=2, column=0, sticky="w", pady=5)
        self.email_entry = tk.Entry(info_frame, width=20)
        self.email_entry.insert(0, self.current_user.email)
        self.email_entry.grid(row=2, column=1, pady=5, padx=(10, 0))

        # User type (read-only)
        type_label = tk.Label(info_frame, text="Tipo:", font=("Helvetica", 8, "bold"))
        type_label.grid(row=3, column=0, sticky="w", pady=5)
        user_type_display = "Professor" if self.current_user.user_type == "teacher" else "Estudante"
        self.type_entry = tk.Entry(info_frame, width=20)
        self.type_entry.insert(0, user_type_display)
        self.type_entry.config(state="readonly")
        self.type_entry.grid(row=3, column=1, pady=5, padx=(10, 0))

        # Password change section
        password_frame = tk.Frame(self)
        password_frame.pack(pady=10, padx=10, fill=tk.X)

        password_title = tk.Label(password_frame, text="Alterar Senha", font=("Helvetica", 10, "bold"))
        password_title.pack()

        current_pass_label = tk.Label(password_frame, text="Senha Atual:", font=("Helvetica", 8))
        current_pass_label.pack(anchor="w", pady=(10, 0))
        self.current_pass_entry = tk.Entry(password_frame, show="*", width=20)
        self.current_pass_entry.pack(pady=5)

        new_pass_label = tk.Label(password_frame, text="Nova Senha:", font=("Helvetica", 8))
        new_pass_label.pack(anchor="w", pady=5)
        self.new_pass_entry = tk.Entry(password_frame, show="*", width=20)
        self.new_pass_entry.pack(pady=5)

        confirm_pass_label = tk.Label(password_frame, text="Confirmar Nova Senha:", font=("Helvetica", 8))
        confirm_pass_label.pack(anchor="w", pady=5)
        self.confirm_pass_entry = tk.Entry(password_frame, show="*", width=20)
        self.confirm_pass_entry.pack(pady=5)

        # Buttons
        buttons_frame = tk.Frame(self)
        buttons_frame.pack(pady=20)

        save_button = tk.Button(buttons_frame, text="Salvar Alterações", command=self.save_changes,
                               bg="#4CAF50", fg="white", font=("Helvetica", 8, "bold"))
        save_button.pack(side=tk.LEFT, padx=10)

        back_button = tk.Button(buttons_frame, text="Voltar", command=self.on_back,
                               bg="#2196F3", fg="white", font=("Helvetica", 8, "bold"))
        back_button.pack(side=tk.LEFT, padx=10)

    def load_user_photo(self):
        try:
            if self.current_user.photo_path and os.path.exists(self.current_user.photo_path):
                image = Image.open(self.current_user.photo_path)
                image = image.resize((150, 150), Image.Resampling.LANCZOS)
                self.photo_image = ImageTk.PhotoImage(image)
                self.photo_label.config(image=self.photo_image, text="")
            else:
                self.photo_label.config(text="[Sem foto]", image="")
        except Exception as e:
            self.photo_label.config(text="[Erro ao carregar foto]", image="")
            print(f"Erro ao carregar foto do perfil: {e}")

    def change_photo(self):
        file_path = filedialog.askopenfilename(
            title="Selecionar foto",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if file_path:
            # Copy file to user photos directory
            os.makedirs("user_photos", exist_ok=True)
            filename = f"{self.current_user.username}_photo{os.path.splitext(file_path)[1]}"
            dest_path = os.path.join("user_photos", filename)

            try:
                with open(file_path, 'rb') as src, open(dest_path, 'wb') as dst:
                    dst.write(src.read())

                self.current_user.photo_path = dest_path
                self.load_user_photo()
                messagebox.showinfo("Sucesso", "Foto alterada com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar foto: {e}")

    def save_changes(self):
        # Update user info
        self.current_user.name = self.name_entry.get().strip()
        self.current_user.email = self.email_entry.get().strip()

        # Handle password change
        current_pass = self.current_pass_entry.get()
        new_pass = self.new_pass_entry.get()
        confirm_pass = self.confirm_pass_entry.get()

        if new_pass or confirm_pass:
            if current_pass != self.current_user.password:
                messagebox.showerror("Erro", "Senha atual incorreta.")
                return
            if new_pass != confirm_pass:
                messagebox.showerror("Erro", "Nova senha e confirmação não coincidem.")
                return
            if len(new_pass) < 3:
                messagebox.showerror("Erro", "Nova senha deve ter pelo menos 3 caracteres.")
                return
            self.current_user.password = new_pass

        # Save to file
        users = load_users()
        for i, user in enumerate(users):
            if user.username == self.current_user.username:
                users[i] = self.current_user
                break
        save_users(users)

        messagebox.showinfo("Sucesso", "Perfil atualizado com sucesso!")

        # Clear password fields
        self.current_pass_entry.delete(0, tk.END)
        self.new_pass_entry.delete(0, tk.END)
        self.confirm_pass_entry.delete(0, tk.END)
