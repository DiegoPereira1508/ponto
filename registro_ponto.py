import tkinter as tk
from tkinter import messagebox
import json

# Funções para gerenciar usuários
def carregar_usuarios():
    try:
        with open('usuarios.json', 'r') as f:
            return json.load(f)['usuarios']
    except FileNotFoundError:
        return {}

def cadastrar_usuario(usuario, senha):
    usuarios = carregar_usuarios()
    usuarios[usuario] = senha
    with open('usuarios.json', 'w') as f:
        json.dump({"usuarios": usuarios}, f)

# Tela de Login
def tela_login():
    def validar_login():
        usuario = entry_usuario.get()
        senha = entry_senha.get()
        usuarios = carregar_usuarios()

        if usuario in usuarios and usuarios[usuario] == senha:
            janela_login.destroy()
            iniciar_aplicacao()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos")

    janela_login = tk.Tk()
    janela_login.title("Login - Registro de Ponto")
    janela_login.configure(bg="#B3D9FF")
    janela_login.geometry("300x200")

    tk.Label(janela_login, text="Registro de Ponto", bg="#B3D9FF", font=("Arial", 14)).pack(pady=10)
    tk.Label(janela_login, text="Usuário:", bg="#B3D9FF").pack()
    entry_usuario = tk.Entry(janela_login)
    entry_usuario.pack()

    tk.Label(janela_login, text="Senha:", bg="#B3D9FF").pack()
    entry_senha = tk.Entry(janela_login, show="*")
    entry_senha.pack()

    btn_login = tk.Button(janela_login, text="Entrar", command=validar_login, bg="#0056b3", fg="white")
    btn_login.pack(pady=5)

    btn_cadastro = tk.Button(janela_login, text="Cadastrar", command=tela_cadastro, bg="#28a745", fg="white")
    btn_cadastro.pack(pady=5)

    janela_login.mainloop()

# Tela de Cadastro
def tela_cadastro():
    def cadastrar():
        usuario = entry_usuario.get()
        senha = entry_senha.get()
        if usuario and senha:
            cadastrar_usuario(usuario, senha)
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            janela_cadastro.destroy()
        else:
            messagebox.showerror("Erro", "Usuário e senha são obrigatórios")

    janela_cadastro = tk.Tk()
    janela_cadastro.title("Cadastro - Registro de Ponto")
    janela_cadastro.configure(bg="#B3D9FF")
    janela_cadastro.geometry("300x200")

    tk.Label(janela_cadastro, text="Cadastro", bg="#B3D9FF", font=("Arial", 14)).pack(pady=10)
    tk.Label(janela_cadastro, text="Usuário:", bg="#B3D9FF").pack()
    entry_usuario = tk.Entry(janela_cadastro)
    entry_usuario.pack()

    tk.Label(janela_cadastro, text="Senha:", bg="#B3D9FF").pack()
    entry_senha = tk.Entry(janela_cadastro, show="*")
    entry_senha.pack()

    btn_cadastrar = tk.Button(janela_cadastro, text="Cadastrar", command=cadastrar, bg="#28a745", fg="white")
    btn_cadastrar.pack(pady=10)

    janela_cadastro.mainloop()

# Iniciar o app
if __name__ == "__main__":
    tela_login()
