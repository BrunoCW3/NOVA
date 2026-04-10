import tkinter as tk
from tkinter import simpledialog, messagebox
import os
import threading
import sys
import subprocess
from core.ai import gerar_stream

BASE_PATH = os.path.join(os.getenv("LOCALAPPDATA"), "NOVA", "memory")
SAVE_PATH = os.path.join(os.getenv("LOCALAPPDATA"), "NOVA", "saved_chats")
CONFIG_PATH = os.path.join(os.getenv("LOCALAPPDATA"), "NOVA", "config.txt")

MODELOS = ["phi3", "llama3:8b", "mixtral"]


def garantir_pastas():
    os.makedirs(BASE_PATH, exist_ok=True)
    os.makedirs(SAVE_PATH, exist_ok=True)

    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w") as f:
            f.write("phi3")


def carregar_modelo():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return f.read().strip()
    return "phi3"


def salvar_modelo(nome):
    with open(CONFIG_PATH, "w") as f:
        f.write(nome)


def salvar_txt(nome, texto):
    with open(os.path.join(BASE_PATH, f"{nome}.txt"), "w", encoding="utf-8") as f:
        f.write(texto)


def listar_memorias():
    return [f for f in os.listdir(BASE_PATH) if f.endswith(".txt")]


def listar_chats():
    return [f for f in os.listdir(SAVE_PATH) if f.endswith(".txt")]


def criar_interface():
    garantir_pastas()

    root = tk.Tk()
    root.title("NOVA")
    root.geometry("900x700")
    root.configure(bg="#1e1e1e")

    stop_flag = {"stop": False}

    # ================= TOPO =================
    top = tk.Frame(root, bg="#1e1e1e")
    top.pack(fill="x")

    modelo_atual = carregar_modelo()

    # -------- ADD MEMORIA (AGORA GRANDE) --------
    def add_mem():
        nome = simpledialog.askstring("Nome", "Nome da memória:")
        if not nome:
            return

        if os.path.exists(os.path.join(BASE_PATH, f"{nome}.txt")):
            messagebox.showerror("Erro", "Já existe")
            return

        janela = tk.Toplevel()
        janela.title("Memória longa")
        janela.geometry("400x300")

        text = tk.Text(janela)
        text.pack(expand=True, fill="both")

        def salvar():
            conteudo = text.get("1.0", tk.END)
            salvar_txt(nome, conteudo)
            janela.destroy()

        tk.Button(janela, text="Salvar", command=salvar).pack()

    # -------- SAVE CHAT --------
    def salvar_chat():
        nome = simpledialog.askstring("Salvar", "Nome do arquivo:")
        if not nome:
            return

        conteudo = chat.get("1.0", tk.END)

        with open(os.path.join(SAVE_PATH, f"{nome}.txt"), "w", encoding="utf-8") as f:
            f.write(conteudo)

        messagebox.showinfo("Salvo", "Chat salvo com sucesso")

    # -------- OPEN CHAT --------
    def abrir_lista():
        janela = tk.Toplevel()
        janela.title("Chats salvos")
        janela.geometry("400x400")

        for arq in listar_chats():
            frame = tk.Frame(janela)
            frame.pack(fill="x")

            tk.Label(frame, text=arq).pack(side="left")

            def abrir(a=arq):
                subprocess.Popen(["notepad.exe", os.path.join(SAVE_PATH, a)])

            def deletar(a=arq):
                os.remove(os.path.join(SAVE_PATH, a))
                janela.destroy()
                abrir_lista()

            tk.Button(frame, text="Open", command=abrir).pack(side="right")
            tk.Button(frame, text="Delete", command=deletar).pack(side="right")

    # -------- MODEL --------
    def escolher_modelo():
        janela = tk.Toplevel()
        for modelo in MODELOS:
            def selecionar(m=modelo):
                salvar_modelo(m)
                root.destroy()
                os.execl(sys.executable, sys.executable, *sys.argv)

            tk.Button(janela, text=modelo, command=selecionar).pack(fill="x")

    # -------- RESET --------
    def reset_app():
        root.destroy()
        os.execl(sys.executable, sys.executable, *sys.argv)

    # Layout
    left = tk.Frame(top, bg="#1e1e1e")
    left.pack(side="left")

    center = tk.Frame(top, bg="#1e1e1e")
    center.pack(side="left", expand=True)

    right = tk.Frame(top, bg="#1e1e1e")
    right.pack(side="right")

    tk.Button(left, text="Add", command=add_mem).pack(side="left")
    tk.Button(left, text="Manage").pack(side="left")
    tk.Button(left, text="Save", command=salvar_chat).pack(side="left")
    tk.Button(left, text="Open", command=abrir_lista).pack(side="left")

    tk.Label(center, text=f"Modelo atual: {modelo_atual}", fg="white", bg="#1e1e1e").pack()

    tk.Button(right, text="Reset", command=reset_app).pack(side="right")
    tk.Button(right, text="Model", command=escolher_modelo).pack(side="right")

    # ================= CHAT =================
    chat_frame = tk.Frame(root)
    chat_frame.pack(fill="both", expand=True)

    chat = tk.Text(
        chat_frame,
        wrap="word",
        bg="#2a2a2a",
        fg="white",
        insertbackground="white",
        selectbackground="#33ccff",
        selectforeground="#000000"
    )
    chat.pack(side="left", fill="both", expand=True)

    scroll = tk.Scrollbar(chat_frame, command=chat.yview)
    scroll.pack(side="right", fill="y")
    chat.config(yscrollcommand=scroll.set)

    def bloquear_edicao(event):
        if event.state & 0x4:
            return
        return "break"

    chat.bind("<Key>", bloquear_edicao)

    # ================= INPUT =================
    bottom = tk.Frame(root)
    bottom.pack(fill="x")

    entrada = tk.Text(bottom, height=3)
    entrada.pack(side="left", fill="x", expand=True)

    status = tk.Label(bottom, text="", fg="white", bg="#1e1e1e")
    status.pack(side="right")

    def spinner():
        estados = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
        i = 0
        while not stop_flag["stop"]:
            status.config(text=f"NOVA pensando {estados[i%len(estados)]}")
            i += 1
            root.update_idletasks()
            root.after(100)

    def escrever(txt):
        chat.insert(tk.END, txt)
        chat.see(tk.END)

    def enviar():
        stop_flag["stop"] = False

        texto = entrada.get("1.0", tk.END).strip()
        if not texto:
            return

        escrever(f"\nUSUÁRIO:\n{texto}\n\nNOVA:\n")
        entrada.delete("1.0", tk.END)

        threading.Thread(target=spinner, daemon=True).start()

        def rodar():
            for parte in gerar_stream(texto, stop_flag):
                if stop_flag["stop"]:
                    break
                chat.after(0, escrever, parte)

            stop_flag["stop"] = True
            status.config(text="")

        threading.Thread(target=rodar, daemon=True).start()

    def cancelar():
        stop_flag["stop"] = True
        status.config(text="Cancelado")

    tk.Button(bottom, text="Enviar", command=enviar).pack(side="left")
    tk.Button(bottom, text="Cancelar", command=cancelar).pack(side="left")

    def enter(e):
        entrada.insert(tk.INSERT, "\n")
        return "break"

    def shift_enter(e):
        enviar()
        return "break"

    entrada.bind("<Return>", enter)
    entrada.bind("<Shift-Return>", shift_enter)

    root.mainloop()