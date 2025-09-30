import tkinter as tk
from tkinter import messagebox, font, ttk
from data import load_users, save_users, User
from lista import EtecListFrame
from etec_details import EtecDetailsFrame
from blog import BlogFrame
from profile import ProfileFrame

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Avaliação das Etecs")
        self.geometry("800x600")
        self.configure(bg="#f0f0f0")
        self.current_user = None

        # Initialize frames
        self.login_frame = LoginFrame(self)
        self.register_frame = RegisterFrame(self)
        self.main_menu_frame = None
        self.etec_list_frame = None
        self.etec_details_frame = None
        self.blog_frame = None
        self.profile_frame = None

        self.show_login()

    def show_login(self):
        # Hide all frames
        self.register_frame.grid_forget()
        if self.main_menu_frame:
            self.main_menu_frame.pack_forget()
        if self.etec_list_frame:
            self.etec_list_frame.pack_forget()
        if self.etec_details_frame:
            self.etec_details_frame.pack_forget()
        if self.blog_frame:
            self.blog_frame.pack_forget()
        if self.profile_frame:
            self.profile_frame.pack_forget()

        self.login_frame.grid()

    def show_register(self):
        self.login_frame.grid_forget()
        self.register_frame.grid()

    def show_main_menu(self):
        self.login_frame.grid_forget()
        self.register_frame.grid_forget()
        if self.etec_list_frame:
            self.etec_list_frame.pack_forget()
        if self.etec_details_frame:
            self.etec_details_frame.pack_forget()
        if self.blog_frame:
            self.blog_frame.pack_forget()
        if self.profile_frame:
            self.profile_frame.pack_forget()
        if not self.main_menu_frame:
            self.main_menu_frame = MainMenuFrame(self)
        self.main_menu_frame.pack(fill=tk.BOTH, expand=True)

    def show_etec_list(self):
        # Hide other frames
        if self.main_menu_frame:
            self.main_menu_frame.pack_forget()
        if self.etec_details_frame:
            self.etec_details_frame.pack_forget()
        if self.blog_frame:
            self.blog_frame.pack_forget()
        if self.profile_frame:
            self.profile_frame.pack_forget()

        if not self.etec_list_frame:
            self.etec_list_frame = EtecListFrame(self, self.show_etec_details)
        self.etec_list_frame.pack(fill=tk.BOTH, expand=True)

    def show_etec_details(self, etec):
        if self.etec_list_frame:
            self.etec_list_frame.pack_forget()
        if self.etec_details_frame:
            self.etec_details_frame.pack_forget()

        self.etec_details_frame = EtecDetailsFrame(self, etec, self.current_user, self.show_etec_list)
        self.etec_details_frame.pack(fill=tk.BOTH, expand=True)

    def show_blog(self):
        self.main_menu_frame.pack_forget()
        if self.etec_list_frame:
            self.etec_list_frame.pack_forget()
        if self.etec_details_frame:
            self.etec_details_frame.pack_forget()
        if self.profile_frame:
            self.profile_frame.pack_forget()

        if not self.blog_frame:
            self.blog_frame = BlogFrame(self)
        self.blog_frame.pack(fill=tk.BOTH, expand=True)

    def show_profile(self):
        self.main_menu_frame.pack_forget()
        if self.etec_list_frame:
            self.etec_list_frame.pack_forget()
        if self.etec_details_frame:
            self.etec_details_frame.pack_forget()
        if self.blog_frame:
            self.blog_frame.pack_forget()

        if not self.profile_frame:
            self.profile_frame = ProfileFrame(self, self.current_user, self.show_main_menu)
        self.profile_frame.pack(fill=tk.BOTH, expand=True)

    def logout(self):
        self.current_user = None
        self.show_login()

class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f0f0f0", padx=20, pady=20)
        self.master = master

        self.custom_font = font.Font(family="Helvetica", size=10, weight="bold")

        self.username_label = tk.Label(self, text="Usuário:", bg="#f0f0f0", font=self.custom_font)
        self.username_label.grid(row=0, column=0, sticky="w", pady=(0,5))
        self.username_entry = tk.Entry(self, width=30)
        self.username_entry.grid(row=1, column=0, pady=(0,10))

        self.password_label = tk.Label(self, text="Senha:", bg="#f0f0f0", font=self.custom_font)
        self.password_label.grid(row=2, column=0, sticky="w", pady=(0,5))
        self.password_entry = tk.Entry(self, show="*", width=30)
        self.password_entry.grid(row=3, column=0, pady=(0,10))

        self.login_button = tk.Button(self, text="Login", command=self.login, bg="#4CAF50", fg="white", width=28, height=1)
        self.login_button.grid(row=4, column=0, pady=(0,10))

        self.register_button = tk.Button(self, text="Ir para Cadastro", command=master.show_register, bg="#2196F3", fg="white", width=28, height=1)
        self.register_button.grid(row=5, column=0)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        users = load_users()
        user = next((u for u in users if u.username == username and u.password == password), None)
        if user:
            self.master.current_user = user
            messagebox.showinfo("Sucesso", f"Login realizado! Bem-vindo, {user.username}")
            self.master.show_main_menu()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos")

class RegisterFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f0f0f0", padx=20, pady=20)
        self.master = master

        self.custom_font = font.Font(family="Helvetica", size=10, weight="bold")

        self.username_label = tk.Label(self, text="Usuário:", bg="#f0f0f0", font=self.custom_font)
        self.username_label.grid(row=0, column=0, sticky="w", pady=(0,5))
        self.username_entry = tk.Entry(self, width=30)
        self.username_entry.grid(row=1, column=0, pady=(0,10))

        self.password_label = tk.Label(self, text="Senha:", bg="#f0f0f0", font=self.custom_font)
        self.password_label.grid(row=2, column=0, sticky="w", pady=(0,5))
        self.password_entry = tk.Entry(self, show="*", width=30)
        self.password_entry.grid(row=3, column=0, pady=(0,10))

        self.confirm_label = tk.Label(self, text="Confirmar Senha:", bg="#f0f0f0", font=self.custom_font)
        self.confirm_label.grid(row=4, column=0, sticky="w", pady=(0,5))
        self.confirm_entry = tk.Entry(self, show="*", width=30)
        self.confirm_entry.grid(row=5, column=0, pady=(0,10))

        self.register_button = tk.Button(self, text="Cadastrar", command=self.register, bg="#4CAF50", fg="white", width=28, height=1)
        self.register_button.grid(row=6, column=0, pady=(0,10))

        self.login_button = tk.Button(self, text="Ir para Login", command=master.show_login, bg="#2196F3", fg="white", width=28, height=1)
        self.login_button.grid(row=7, column=0)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()
        if password != confirm:
            messagebox.showerror("Erro", "Senhas não coincidem")
        elif not username or not password:
            messagebox.showerror("Erro", "Preencha todos os campos")
        else:
            users = load_users()
            if any(u.username == username for u in users):
                messagebox.showerror("Erro", "Usuário já existe")
                return

            new_user = User(username, password, user_type="student")
            users.append(new_user)
            save_users(users)
            messagebox.showinfo("Sucesso", "Cadastro realizado!")
            self.master.show_login()

class MainMenuFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f0f0f0", padx=20, pady=20)
        self.pack(fill=tk.BOTH, expand=True)
        self.master = master

        self.label = tk.Label(self, text="Avaliador de etecs", font=("Helvetica", 18, "bold"), bg="#f0f0f0")
        self.label.pack(pady=20)

        # Welcome message
        welcome_text = f"Bem-vindo, {master.current_user.username}!" if master.current_user else "Bem-vindo!"
        self.welcome_label = tk.Label(self, text=welcome_text,
                                     font=("Helvetica", 12), bg="#f0f0f0")
        self.welcome_label.pack(pady=10)

        # Menu buttons
        button_frame = tk.Frame(self, bg="#f0f0f0")
        button_frame.pack(pady=30)

        self.etec_list_button = tk.Button(button_frame, text="Lista de Etecs", command=master.show_etec_list,
                                         bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"),
                                         width=20, height=2)
        self.etec_list_button.pack(pady=10)

        self.blog_button = tk.Button(button_frame, text="Blog de Avaliações", command=master.show_blog,
                                    bg="#2196F3", fg="white", font=("Helvetica", 12, "bold"),
                                    width=20, height=2)
        self.blog_button.pack(pady=10)

        self.profile_button = tk.Button(button_frame, text="Meu Perfil", command=master.show_profile,
                                       bg="#FF9800", fg="white", font=("Helvetica", 12, "bold"),
                                       width=20, height=2)
        self.profile_button.pack(pady=10)

        self.logout_button = tk.Button(button_frame, text="Sair", command=master.logout,
                                      bg="#f44336", fg="white", font=("Helvetica", 12, "bold"),
                                      width=20, height=2)
        self.logout_button.pack(pady=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()
