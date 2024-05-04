import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from tkinter import ttk
import shutil

class RankingPastasApp:
    def __init__(self, master):
        self.master = master

        #definicoes de caracteristicas da janela
        master.title("Ranking de Pastas")  
        master.geometry("800x480")  
        master.configure(bg="black")  

        #label p/ instrucoes
        self.label = tk.Label(master, text="Selecione uma pasta para ver o Top 5 pastas por tamanho:", fg="white", bg="black", font=("Arial", 16))
        self.label.pack(pady=20)

        #botao p/ selecionar
        self.selecionar_button = tk.Button(master, text="Selecionar Pasta", command=self.selecionar_pasta, bg="white", fg="black", width=40, height=4, font=("Arial", 16))
        self.selecionar_button.pack(pady=20)

        #botao de fechar
        self.fechar_button = tk.Button(master, text="Fechar", command=self.fechar, bg="white", fg="black", width=40, height=4, font=("Arial", 16))
        self.fechar_button.pack()

    def calcular_tamanho_pasta(self, caminho):
        total_tamanho = 0
        for pasta_atual, pastas, arquivos in os.walk(caminho):
            for arquivo in arquivos:
                try:
                    caminho_arquivo = os.path.join(pasta_atual, arquivo)
                    total_tamanho += os.path.getsize(caminho_arquivo)
                except OSError:
                    #ignoramos os erros de permissao
                    pass
        return total_tamanho

    def bytes_para_gb(self, tamanho_em_bytes):
        return tamanho_em_bytes / (1024 ** 3)  #conversao de byte p/ gb

    def rank_top5_pasta_por_tamanho(self, caminho_pasta):
        pastas = []

        #lista todas as pastas dentro da pasta fornecida
        for pasta in os.listdir(caminho_pasta):
            caminho_completo = os.path.join(caminho_pasta, pasta)
            if os.path.isdir(caminho_completo):
                tamanho = self.calcular_tamanho_pasta(caminho_completo)
                pastas.append((pasta, tamanho))

        #ordena as pastas por tamanho
        pastas_ordenadas = sorted(pastas, key=lambda x: x[1], reverse=True)

        return pastas_ordenadas[:5]     #retorna as 5 maiores

    def selecionar_pasta(self):
        #abre a caixa de dialogo
        caminho_pasta = filedialog.askdirectory()
        if caminho_pasta:
            top5_pasta = self.rank_top5_pasta_por_tamanho(caminho_pasta)
            self.mostrar_resultados(caminho_pasta, top5_pasta)

    def mostrar_resultados(self, caminho_pasta, top5_pasta):
        self.caminho_pasta = caminho_pasta
        self.label.config(text=f"Top 5 pastas por tamanho em {caminho_pasta}:")
        self.selecionar_button.config(text="Selecionar Outra Pasta", command=self.selecionar_pasta)
        
        #nova janela, para os resultados
        self.resultado_window = tk.Toplevel(self.master)
        self.resultado_window.title("Resultado")
        self.resultado_window.geometry("800x480")
        self.resultado_window.configure(bg="black")
        
        resultado_label = tk.Label(self.resultado_window, text="Top 5 pastas por tamanho:", fg="white", bg="black", font=("Arial", 16))
        resultado_label.pack()

        #combobox p/ as pastas
        self.combobox = ttk.Combobox(self.resultado_window, values=[pasta[0] for pasta in top5_pasta], state="readonly")
        self.combobox.pack(pady=10)

        #botao p/ deletar
        self.deletar_button = tk.Button(self.resultado_window, text="Deletar Pasta", command=self.deletar_pasta, bg="white", fg="black", width=20, height=2, font=("Arial", 16))
        self.deletar_button.pack(pady=20)

    def deletar_pasta(self):
        pasta_selecionada = self.combobox.get()
        if not pasta_selecionada:
            messagebox.showerror("Erro", "Selecione uma pasta para deletar.")
            return

        #confirmacao de delete
        resposta = messagebox.askquestion("Confirmar", f"Tem certeza que deseja deletar a pasta '{pasta_selecionada}'?")
        if resposta == "yes":
            pasta_completa = os.path.join(self.caminho_pasta, pasta_selecionada)
            try:
                shutil.rmtree(pasta_completa)
                messagebox.showinfo("Aviso", f"Pasta '{pasta_selecionada}' deletada com sucesso!")
            except OSError as e:
                messagebox.showerror("Erro", f"Erro ao deletar pasta: {e}")
            
            self.resultado_window.destroy()
            self.label.config(text="Selecione uma pasta para ver o Top 5 pastas por tamanho:")
            self.selecionar_button.config(text="Selecionar Pasta", command=self.selecionar_pasta)

    def fechar(self):
        self.master.destroy()

root = tk.Tk()
app = RankingPastasApp(root)
root.mainloop()
