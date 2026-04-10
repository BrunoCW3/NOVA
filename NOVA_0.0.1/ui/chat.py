import tkinter as tk
from tkinter import simpledialog, messagebox
import pyperclip
import os
import threading
from core.ai import gerar_stream

BASE_PATH = os.path.join(os.getenv("LOCALAPPDATA"), "NOVA", "memory")


def garantir_pasta():
    os.makedirs(BASE_PATH, exist_ok=True)


def listar_memorias():
    return [f for f in os.listdir(BASE_PATH) if f.endswith(".txt")]


def salvar_memoria(nome, texto):
    with open(os.path.join(BASE_PATH, f"{nome}.txt"), "w", encoding="utf-8") as f:
        f.write(texto)


def abrir_memoria():
    nome = simpledialog.askstring("Nome", "Nome da memória:")
    if not nome:
        return

    caminho = os.path.join(BASE_PATH, f"{nome}.txt")

    if os.path.exists(caminho):
        messagebox.showerror("Erro", "Nome já existe")
        return abrir_memoria()

    texto = simpledialog.askstring("Conteúdo", "Conteúdo:")
    if texto:
        salvar_memoria(nome, texto)


def abrir_gerenciador():
    janela = tk.Toplevel()
    janela.title("Memórias")
    janela.geometry("400x400")
    janela.configure(bg="#1e1e1e")

    for mem in listar_memorias():
        nome = mem.replace(".txt", "")

        linha = tk.Frame(janela, bg="#1e1e1e")
        linha.pack(fill="x", pady=5)

        tk.Label(linha, text=nome, fg="white", bg="#1e1e1e").pack(side="left")

        def view(n=nome):
            with open(os.path.join(BASE_PATH, f"{n}.txt"), "r", encoding="utf-8") as f:
                messagebox.showinfo(n, f.read())

        def edit(n=nome):
            texto = simpledialog.askstring("Editar", f"{n}:")
            if texto:
                salvar_memoria(n, texto)

        def delete(n=nome):
            if messagebox.askyesno("Confirmação", "Deletar?"):
                os.remove(os.path.join(BASE_PATH, f"{n}.txt"))
                janela.destroy()
                abrir_gerenciador()

        tk.Button(linha, text="View", command=view).pack(side="right")
        tk.Button(linha, text="Edit", command=edit).pack(side="right")
        tk.Button(linha, text="Delete", command=delete).pack(side="right")


def copiar_texto(texto):
    pyperclip.copy(texto)


def criar_interface():
    garantir_pasta()

    root = tk.Tk()
    root.title("NOVA")
    root.geometry("700x600")
    root.configure(bg="#1e1e1e")

    top = tk.Frame(root, bg="#1e1e1e")
    top.pack(anchor="nw")

    tk.Button(top, text="Add", command=abrir_memoria).pack(side="left")
    tk.Button(top, text="Manage", command=abrir_gerenciador).pack(side="left")

    canvas = tk.Canvas(root, bg="#1e1e1e")
    frame = tk.Frame(canvas, bg="#1e1e1e")
    scroll = tk.Scrollbar(root, command=canvas.yview)

    canvas.configure(yscrollcommand=scroll.set)
    scroll.pack(side="right", fill="y")
    canvas.pack(fill="both", expand=True)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    def atualizar_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", atualizar_scroll)

    entrada = tk.Text(root, height=3)
    entrada.pack(fill="x")

    ultima = {"texto": ""}

    def add_msg(texto, lado="left"):
        box = tk.Frame(frame, bg="#1e1e1e")
        box.pack(anchor=lado, pady=5)

        label = tk.Label(
            box,
            text=texto,
            bg="#2d2d2d",
            fg="white",
            wraplength=400,
            justify="left",
            padx=10,
            pady=5
        )
        label.pack()

        return label

    def enviar(event=None):
        texto = entrada.get("1.0", tk.END).strip()
        if not texto:
            return "break"

        add_msg(texto, "e")

        entrada.delete("1.0", tk.END)

        ultima["texto"] = ""
        label = add_msg("", "w")

        def rodar():
            for parte in gerar_stream(texto):
                ultima["texto"] += parte
                root.after(0, lambda p=parte: label.config(text=label.cget("text") + p))

            root.after(0, lambda: tk.Button(
                frame,
                text="Copiar",
                command=lambda: copiar_texto(ultima["texto"])
            ).pack())

        threading.Thread(target=rodar, daemon=True).start()

        return "break"

    entrada.bind("<Return>", enviar)

    def shift_enter(event):
        entrada.insert(tk.INSERT, "\n")
        return "break"

    entrada.bind("<Shift-Return>", shift_enter)

    root.mainloop()