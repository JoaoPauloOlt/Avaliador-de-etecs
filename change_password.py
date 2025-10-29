import tkinter as tk
from tkinter import messagebox
from data import load_users, save_users

class ChangePasswordFrame(tk.Frame):
    def __init__(self, master, current_user, on_back):
        super().__init__(master)
        self.master = master
        self.current_user = current_user
        self.on_back = on_back

        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self, text="Alterar Senha", font=("Helvetica", 12, "bold"))
        title_label.pack(pady=10)

        # Password fields
        fields_frame = tk.Frame(self)
        fields_frame.pack(pady=20, padx=10, fill=tk.X)

        current_pass_label = tk.Label(fields_frame, text="Senha Atual:", font=("Helvetica", 8, "bold"))
        current_pass_label.grid(row=0, column=0, sticky="w", pady=5)
        self.current_pass_entry = tk.Entry(fields_frame, show="*", width=20)
        self.current_pass_entry.grid(row=0, column=1, pady=5, padx=(10, 0))

        new_pass_label = tk.Label(fields_frame, text="Nova Senha:", font=("Helvetica", 8, "bold"))
        new_pass_label.grid(row=1, column=0, sticky="w", pady=5)
        self.new_pass_entry = tk.Entry(fields_frame, show="*", width=20)
        self.new_pass_entry.grid(row=1, column=1, pady=5, padx=(10, 0))

        confirm_pass_label = tk.Label(fields_frame, text="Confirmar Nova Senha:", font=("Helvetica", 8, "bold"))
        confirm_pass_label.grid(row=2, column=0, sticky="w", pady=5)
        self.confirm_pass_entry = tk.Entry(fields_frame, show="*", width=20)
        self.confirm_pass_entry.grid(row=2, column=1, pady=5, padx=(10, 0))

        # Buttons
        buttons_frame = tk.Frame(self)
        buttons_frame.pack(pady=20)

        save_button = tk.Button(buttons_frame, text="Salvar Senha", command=self.save_password,
                               bg="#4CAF50", fg="white", font=("Helvetica", 8, "bold"))
        save_button.pack(side=tk.LEFT, padx=10)

        back_button = tk.Button(buttons_frame, text="Voltar", command=self.on_back,
                               bg="#2196F3", fg="white", font=("Helvetica", 8, "bold"))
        back_button.pack(side=tk.LEFT, padx=10)

    def save_password(self):
        current_pass = self.current_pass_entry.get()
        new_pass = self.new_pass_entry.get()
        confirm_pass = self.confirm_pass_entry.get()

        if not current_pass or not new_pass or not confirm_pass:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

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

        messagebox.showinfo("Sucesso", "Senha alterada com sucesso!")

        # Clear fields
        self.current_pass_entry.delete(0, tk.END)
        self.new_pass_entry.delete(0, tk.END)
        self.confirm_pass_entry.delete(0, tk.END)

        # Go back
        self.on_back()
