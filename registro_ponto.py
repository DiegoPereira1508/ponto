import tkinter as tk
from tkinter import messagebox
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

# Configurações básicas
EMAIL_DESTINO = "diego.pereira1508@gmail.com"
TAXAS_HORA = {
    "Elétrica": 103.00,
    "Manutenção civil": 97.00,
    "Hidraulica": 97.50
}

# Função para enviar e-mail
def enviar_email(arquivo):
    msg = MIMEMultipart()
    msg['From'] = 'seuemail@gmail.com'
    msg['To'] = EMAIL_DESTINO
    msg['Subject'] = 'Registro de Ponto Diário'

    corpo = "Segue em anexo o registro de ponto do dia."
    msg.attach(MIMEText(corpo, 'plain'))

    with open(arquivo, "rb") as f:
        parte = MIMEApplication(f.read(), Name=os.path.basename(arquivo))
    parte['Content-Disposition'] = f'attachment; filename="{os.path.basename(arquivo)}"'
    msg.attach(parte)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('seuemail@gmail.com', 'suasenha')
        server.send_message(msg)
        server.quit()
        messagebox.showinfo("Sucesso", "Registro enviado por e-mail.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao enviar e-mail: {str(e)}")

# Função para salvar e enviar PDF
def salvar_e_enviar_pdf(registros):
    hoje = datetime.datetime.now().strftime("%Y-%m-%d")
    nome_pdf = f"registro_ponto_{hoje}.pdf"

    with open(nome_pdf, "w") as f:
        f.write("Registro de Ponto - Diário\n")
        for reg in registros:
            f.write(f"{reg[0]} | {reg[1]} | {reg[2]} | {reg[3]}\n")

    enviar_email(nome_pdf)
    os.startfile(nome_pdf)

# Função principal da aplicação
def iniciar_aplicacao():
    registros = []

    def registrar_entrada():
        agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        funcao = funcao_var.get()
        registros.append([agora, funcao, "", ""])
        atualizar_lista()

    def registrar_saida():
        if not registros or registros[-1][2] != "":
            messagebox.showwarning("Erro", "Não há entrada pendente!")
            return

        agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        registros[-1][2] = agora

        entrada = datetime.datetime.strptime(registros[-1][0], "%Y-%m-%d %H:%M")
        saida = datetime.datetime.strptime(registros[-1][2], "%Y-%m-%d %H:%M")
        minutos_trabalhados = (saida - entrada).seconds // 60
        valor_hora = TAXAS_HORA[registros[-1][1]]
        valor_trabalhado = (minutos_trabalhados / 60) * valor_hora

        registros[-1][3] = f"R$ {valor_trabalhado:.2f}"
        atualizar_lista()
        salvar_e_enviar_pdf(registros)

    def atualizar_lista():
        lista_registros.delete(0, tk.END)
        for reg in registros:
            lista_registros.insert(tk.END, f"{reg[0]} | {reg[1]} | {reg[2]} | {reg[3]}")

    # Configuração da janela principal
    janela = tk.Tk()
    janela.title("Registro de Ponto")
    janela.geometry("500x400")

    tk.Label(janela, text="Função:").pack()
    funcao_var = tk.StringVar(value="Elétrica")
    tk.OptionMenu(janela, funcao_var, "Elétrica", "Manutenção civil", "Hidraulica").pack()

    tk.Button(janela, text="Registrar Entrada", command=registrar_entrada).pack(pady=5)
    tk.Button(janela, text="Registrar Saída", command=registrar_saida).pack(pady=5)

    lista_registros = tk.Listbox(janela, width=70, height=15)
    lista_registros.pack(pady=10)

    tk.Button(janela, text="Sair", command=janela.destroy).pack(pady=5)

    janela.mainloop()

# Iniciar a aplicação
if __name__ == "__main__":
    iniciar_aplicacao()