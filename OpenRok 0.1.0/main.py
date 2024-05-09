import tkinter as tk
from tkinter import Menu, messagebox, Listbox, Scrollbar
from ttkthemes import ThemedTk
from PIL import ImageGrab
import cv2
import numpy as np
import json
from analise import analisar_ocr

class CapturaTela:
    def __init__(self):
        self.janela = ThemedTk(theme="arc")
        self.janela.title("OpenRok")
        self.janela.geometry("250x350")
        self.janela.iconbitmap("logo.ico")


        self.label_pergunta = tk.Label(
            self.janela, text="Pergunta:", font=("Arial", 12, "bold")
        )
        self.label_pergunta.pack(pady=5)

        self.label_resultado_pergunta = tk.Label(
            self.janela, text="", wraplength=200, justify="center", font=("Arial", 10)
        )
        self.label_resultado_pergunta.pack(pady=5)

        self.label_resposta = tk.Label(
            self.janela, text="Resposta:", font=("Arial", 12, "bold")
        )
        self.label_resposta.pack(pady=5)

        self.label_resultado_resposta = tk.Label(
            self.janela,
            text="",
            wraplength=200,
            justify="center",
            font=("Arial", 14, "bold"),
        )
        self.label_resultado_resposta.pack(pady=5)

        self.menu_principal = Menu(self.janela)
        self.janela.config(menu=self.menu_principal)

        self.menu_sobre = Menu(self.menu_principal, tearoff=0)
        self.menu_principal.add_cascade(label="Sobre", menu=self.menu_sobre)
        self.menu_sobre.add_command(label="Versão", command=self.versao)
        self.menu_sobre.add_command(label="Contato", command=self.contato)

        self.menu_area = Menu(self.menu_principal, tearoff=0)
        self.menu_principal.add_cascade(label="Área de Captura", menu=self.menu_area)
        self.menu_area.add_command(
            label="Definir Coordenadas", command=self.definir_area
        )
        self.menu_area.add_command(
            label="Salvar Coordenada", command=self.salvar_coordenada
        )
        self.menu_area.add_command(
            label="Carregar Coordenada", command=self.carregar_coordenada
        )

        self.botao_capturar = tk.Button(
            self.janela,
            text="Pesquisar",
            command=self.analisar_imagem,
            font=("Arial", 10),
        )
        self.botao_capturar.pack(side=tk.TOP, pady=10)

        self.var_fixar_janela = tk.BooleanVar()
        self.botao_fixar = tk.Checkbutton(
            self.janela,
            text="Fixar Janela",
            variable=self.var_fixar_janela,
            command=self.fixar_janela,
            font=("Arial", 10),
        )
        self.botao_fixar.pack(side=tk.TOP, pady=5)

        self.botao_copiar_texto = tk.Button(
            self.janela,
            text="Copiar pergunta",
            command=self.copiar_texto,
            state=tk.DISABLED,
            font=("Arial", 10),
        )
        self.botao_copiar_texto.pack(side=tk.TOP, pady=5)

        self.coordenadas = []
        self.coordenada_atual = None
        self.carregar_coordenadas_salvas()

        self.janela.mainloop()

    def versao(self):
        messagebox.showinfo("Versão", "Versão 0.1.0")

    def contato(self):
        messagebox.showinfo("Contato", "Discord: jetblue._.")

    def definir_area(self):

        self.janela.attributes("-alpha", 0.01)

        imagem = ImageGrab.grab()
        imagem_np = np.array(imagem)
        imagem = cv2.cvtColor(imagem_np, cv2.COLOR_RGB2BGR)

        cv2.namedWindow("Selecione a area", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(
            "Selecione a area", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL
        )

        cv2.resizeWindow(
            "Selecione a area",
            self.janela.winfo_screenwidth(),
            self.janela.winfo_screenheight(),
        )

        roi = cv2.selectROI("Selecione a area", imagem)
        self.coordenada_atual = roi

        self.janela.attributes("-alpha", 1.0)
        self.janela.deiconify()

    def salvar_coordenada(self):
        if self.coordenada_atual:
            self.coordenadas.append(self.coordenada_atual)
            self.salvar_coordenadas()
            messagebox.showinfo(
                "Coordenada Salva", "A coordenada foi salva com sucesso."
            )
        else:
            messagebox.showwarning(
                "Nenhuma Coordenada", "Nenhuma coordenada foi definida."
            )

    def carregar_coordenada(self):
        if self.coordenadas:
            selecionar_janela = tk.Toplevel(self.janela)
            selecionar_janela.title("Escolha a Coordenada")
            selecionar_janela.iconbitmap("logo.ico")

            lb = Listbox(selecionar_janela, selectmode=tk.SINGLE)
            lb.pack()

            for i, coord in enumerate(self.coordenadas):
                lb.insert(tk.END, f"Coordenada {i+1}: {coord}")

            def escolher_coordenada():
                selecionado = lb.curselection()
                if selecionado:
                    indice = selecionado[0]
                    self.coordenada_atual = self.coordenadas[indice]
                    messagebox.showinfo(
                        "Coordenada Escolhida",
                        f"A coordenada {indice+1} foi selecionada.",
                    )
                    selecionar_janela.destroy()
                else:
                    messagebox.showwarning(
                        "Selecionar Coordenada", "Selecione uma coordenada."
                    )

            btn_ok = tk.Button(
                selecionar_janela, text="OK", command=escolher_coordenada
            )
            btn_ok.pack()

        else:
            messagebox.showwarning("Nenhuma Coordenada", "Nenhuma coordenada salva.")

    def salvar_coordenadas(self):
        with open("coordenadas.json", "w") as arquivo:
            json.dump(self.coordenadas, arquivo)

    def carregar_coordenadas_salvas(self):
        try:
            with open("coordenadas.json", "r") as arquivo:
                self.coordenadas = json.load(arquivo)
        except FileNotFoundError:
            self.coordenadas = []
        except json.JSONDecodeError:
            self.coordenadas = []

    def analisar_imagem(self):
        if self.coordenada_atual:
            imagem = ImageGrab.grab(
                bbox=(
                    self.coordenada_atual[0],
                    self.coordenada_atual[1],
                    self.coordenada_atual[0] + self.coordenada_atual[2],
                    self.coordenada_atual[1] + self.coordenada_atual[3],
                )
            )
            imagem.save("analisar.png")

            pergunta, respostas = analisar_ocr(
                "analisar.png", "banco_de_dados.db"
            )

            self.label_resultado_pergunta.config(text=pergunta)
            self.label_resultado_resposta.config(text=respostas)
            self.botao_copiar_texto.config(
                state=(
                    tk.NORMAL
                    if pergunta != "Nenhuma correspondência encontrada."
                    else tk.DISABLED
                )
            )
        else:
            messagebox.showwarning(
                "Nenhuma Coordenada", "Nenhuma coordenada foi definida."
            )

    def fixar_janela(self):
        if self.var_fixar_janela.get():
            self.janela.attributes("-topmost", True)
        else:
            self.janela.attributes("-topmost", False)

    def copiar_texto(self):
        texto = self.label_resultado_pergunta.cget("text")
        self.janela.clipboard_clear()
        self.janela.clipboard_append(texto)
        self.janela.update()
        
if __name__ == "__main__":
    app = CapturaTela()