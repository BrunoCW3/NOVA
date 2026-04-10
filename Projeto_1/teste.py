import tkinter as tk

from tkinter import simpledialog

from tkinter import messagebox


# Criar janela principal do Tkinter.

root = tk.Tk()


# Função para exibir a caixa de diálogo personalizada com uma mensagem e um prompt.

def mostrar_mensagem():

    messagebox.showinfo("Seja Bem-Vindo", "Hello! How are you?")


# Botão que, quando clicado, mostra a caixa de diálogo personalizada com uma mensagem e um prompt para resposta do usuenero.

botao = tk.Button(root, text="Mostrar", command=mostrar_mensagem)

botao.pack()


# Iniciar a janela principal Tkinter.

root.mainloop()