import tkinter as tk
from tkinter import messagebox, font, ttk
from data import load_users, save_users, User
from lista import EtecListFrame
from etec_details import EtecDetailsFrame
from blog import BlogFrame
from profile import ProfileFrame
from change_password import ChangePasswordFrame

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Avaliação das Etecs")
        window_width = 360
        window_height = 640
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)
        self.configure(bg="#f0f0f0")
        self.current_user = None

        self.login_frame = LoginFrame(self)
        self.register_frame = RegisterFrame(self)
        self.main_menu_frame = None
        self.etec_list_frame = None
        self.etec_details_frame = None
        self.blog_frame = None
        self.profile_frame = None
        self.change_password_frame = None

        self.show_login()

    def show_login(self):
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
        else:
            self.main_menu_frame.update_welcome(self.current_user.username if self.current_user else None)
        self.main_menu_frame.pack(fill=tk.BOTH, expand=True)

    def show_etec_list(self):
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
        else:
            self.etec_list_frame.refresh()
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
        if self.change_password_frame:
            self.change_password_frame.pack_forget()

        if not self.profile_frame:
            self.profile_frame = ProfileFrame(self, self.current_user, self.show_main_menu)
        self.profile_frame.pack(fill=tk.BOTH, expand=True)

    def show_change_password(self):
        if self.profile_frame:
            self.profile_frame.pack_forget()

        self.change_password_frame = ChangePasswordFrame(self, self.current_user, self.show_profile)
        self.change_password_frame.pack(fill=tk.BOTH, expand=True)

    def logout(self):
        self.current_user = None
        self.show_login()

class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f0f0f0", padx=10, pady=10)
        self.master = master

        self.custom_font = font.Font(family="Helvetica", size=8, weight="bold")

        container = tk.Frame(self, bg="#f0f0f0")
        container.pack(expand=True)

        self.username_label = tk.Label(container, text="Usuário:", bg="#f0f0f0", font=self.custom_font)
        self.username_label.pack(pady=(0,5))
        self.username_entry = tk.Entry(container, width=20)
        self.username_entry.pack(pady=(0,10))

        self.password_label = tk.Label(container, text="Senha:", bg="#f0f0f0", font=self.custom_font)
        self.password_label.pack(pady=(0,5))
        self.password_entry = tk.Entry(container, show="*", width=20)
        self.password_entry.pack(pady=(0,10))

        self.login_button = tk.Button(container, text="Login", command=self.login, bg="#4CAF50", fg="white", width=20, height=1)
        self.login_button.pack(pady=(0,10))

        self.register_button = tk.Button(container, text="Ir para Cadastro", command=master.show_register, bg="#2196F3", fg="white", width=20, height=1)
        self.register_button.pack()

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
        super().__init__(master, bg="#f0f0f0", padx=10, pady=10)
        self.master = master

        self.custom_font = font.Font(family="Helvetica", size=8, weight="bold")

        container = tk.Frame(self, bg="#f0f0f0")
        container.pack(expand=True)

        self.username_label = tk.Label(container, text="Usuário:", bg="#f0f0f0", font=self.custom_font)
        self.username_label.pack(pady=(0,5))
        self.username_entry = tk.Entry(container, width=20)
        self.username_entry.pack(pady=(0,10))

        self.password_label = tk.Label(container, text="Senha:", bg="#f0f0f0", font=self.custom_font)
        self.password_label.pack(pady=(0,5))
        self.password_entry = tk.Entry(container, show="*", width=20)
        self.password_entry.pack(pady=(0,10))

        self.confirm_label = tk.Label(container, text="Confirmar Senha:", bg="#f0f0f0", font=self.custom_font)
        self.confirm_label.pack(pady=(0,5))
        self.confirm_entry = tk.Entry(container, show="*", width=20)
        self.confirm_entry.pack(pady=(0,10))

        self.user_type_label = tk.Label(container, text="Tipo de Usuário:", bg="#f0f0f0", font=self.custom_font)
        self.user_type_label.pack(pady=(0,5))
        self.user_type_var = tk.StringVar(value="student")
        self.student_radio = tk.Radiobutton(container, text="Estudante", variable=self.user_type_var, value="student", bg="#f0f0f0", font=self.custom_font)
        self.student_radio.pack()
        self.teacher_radio = tk.Radiobutton(container, text="Professor", variable=self.user_type_var, value="teacher", bg="#f0f0f0", font=self.custom_font)
        self.teacher_radio.pack()

        self.register_button = tk.Button(container, text="Cadastrar", command=self.register, bg="#4CAF50", fg="white", width=20, height=1)
        self.register_button.pack(pady=(10,10))

        self.login_button = tk.Button(container, text="Ir para Login", command=master.show_login, bg="#2196F3", fg="white", width=20, height=1)
        self.login_button.pack()

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()
        user_type = self.user_type_var.get() if hasattr(self, 'user_type_var') else "student"
        if password != confirm:
            messagebox.showerror("Erro", "Senhas não coincidem")
        elif not username or not password:
            messagebox.showerror("Erro", "Preencha todos os campos")
        else:
            users = load_users()
            if any(u.username == username for u in users):
                messagebox.showerror("Erro", "Usuário já existe")
                return

            new_user = User(username, password, user_type=user_type)
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

        self.welcome_label = tk.Label(self, text="",
                                     font=("Helvetica", 12), bg="#f0f0f0")
        self.welcome_label.pack(pady=10)
        self.update_welcome(master.current_user.username if master.current_user else None)

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

    def update_welcome(self, username):
        welcome_text = f"Bem-vindo, {username}!" if username else "Bem-vindo!"
        self.welcome_label.config(text=welcome_text)

if __name__ == "__main__":
    app = App()
    app.mainloop()
